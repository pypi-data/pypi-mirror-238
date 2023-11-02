import logging
import sys

import keyring
from PyQt6 import QtCore
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QWidget,
)

from ixontray.ixon_cloud_api import IxonCloudAPIv1
from ixontray.ixon_vpn_client_api import CONNECTION_STATUS, IxonVpnClient
from ixontray.settings_window import ClientsTab
from ixontray.telemetry import log_telemetry
from ixontray.types.api import IXapiApplicationID
from ixontray.types.common import AgentList, Command, Commands


class CommandItem(QListWidgetItem):
    def __init__(self, command: Command) -> None:
        super().__init__(QIcon.fromTheme(command.icon), command.name)
        self._command = command

    def get_command(self) -> Command:
        return self._command

    def set_command(self, command: Command) -> None:
        self._command = command


class CommandOptions(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._layout = QGridLayout()
        self._commands = Commands()
        self._options = QListWidget()
        self._layout.addWidget(self._options)
        self.setLayout(self._layout)

    def set_commands(self, commands: Commands) -> None:
        self._commands = commands
        for cmd in self._commands.commands[::-1]:
            print(cmd.name)
            if "item" in cmd.show_in:
                self._options.addItem(CommandItem(cmd))

        self._options.addItem(QListWidgetItem("No action"))
        self._options.setCurrentRow(0)

    @log_telemetry
    def execute(self) -> None:
        command_item = self._options.currentItem()
        if isinstance(command_item, CommandItem):
            command = command_item.get_command()
            logging.info(f"Running {command.name}")
            command.execute()


class Launcher(QWidget):
    def __init__(self, settings: QSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Ixontray Launcher")
        self.setStyleSheet("""
        font-size: 30pt;
        QLineEdit { background: #333; border: 2px; color: #FFF; padding: 30px; margin:10 px; };
        QListWidget { font-size: 30pt; margin: 10px;}
        """)

        self._agents = AgentList(agents_by_id={})
        self._settings = settings
        self._layout = QHBoxLayout(self)
        self.setLayout(self._layout)

        # Search box
        self.clients_tab = ClientsTab()
        self.clients_tab.lw_all_clients.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.clients_tab.lw_all_clients.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.clients_tab.lw_selected_clients.hide()
        self.clients_tab.btn_move_left.hide()
        self.clients_tab.btn_move_right.hide()
        self.clients_tab.lbl_fav_clients.hide()
        self.clients_tab.lbl_all_clients.hide()
        self._layout.addWidget(self.clients_tab)

        # Add commands options
        self.command_options = CommandOptions(parent=self)
        self._layout.addWidget(self.command_options)

        # self.clients_tab.lw_all_clients.setMinimumWidth(1000)
        # set window hing
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.FramelessWindowHint)
        # Center window
        # self.center()
        # Set focus on search bar
        self.clients_tab.le_search_clients.setFocus()

    def set_commands(self, commands: Commands) -> None:
        self.command_options.set_commands(commands)
        width = self.command_options._options.sizeHintForColumn(0)
        self.command_options._options.setMinimumWidth(int(width * 1.1))

    def set_agents(self, agents: AgentList) -> None:
        self._agents = agents
        self.clients_tab.set_all_clients(clients=agents.agents_by_id, favourites={})
        width = self.clients_tab.lw_all_clients.sizeHintForColumn(0)
        self.clients_tab.lw_all_clients.setMinimumWidth(int(width * 1.1))

    def center(self) -> None:
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, qKeyEvent) -> None:  # noqa
        if qKeyEvent.key() == QtCore.Qt.Key.Key_Return:
            item = self.clients_tab.lw_all_clients.currentItem()
            if item.isHidden():
                self.close()
                return
            agent = item.text()
            agent_id = self.clients_tab.inverted_mapping[agent]
            logging.info(f"Selected agent: {agent} with id {agent_id}")
            self.setEnabled(False)
            self.close()
            self.connect_to_host(agent_id=agent_id)
            self.command_options.execute()

        if qKeyEvent.key() in [QtCore.Qt.Key.Key_Down, QtCore.Qt.Key.Key_Up]:
            self.clients_tab.lw_all_clients.keyPressEvent(qKeyEvent)

        if qKeyEvent.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(qKeyEvent)

    def connect_to_host(self, agent_id: str) -> str:
        """Returns user name and password."""
        username = self._settings.value("email", "")
        password = keyring.get_password("Ixontray", username)
        auth_string = IxonCloudAPIv1.generate_auth(email=username, pwd=password)
        token = IxonCloudAPIv1(application_id=IXapiApplicationID).generate_access_token(auth=auth_string)
        ixon_vpn_client = IxonVpnClient(token=token)
        print(ixon_vpn_client.status())

        connect = True
        if ixon_vpn_client.connected():
            if agent_id in ixon_vpn_client.status().get("agentId", ""):
                print("Already connected to right client not not connecting again.")
                connect = False
            else:
                ixon_vpn_client.disconnect()
                print("Wait for disconnect")
                ixon_vpn_client.wait_for_status(wanted_status=CONNECTION_STATUS.IDLE)

        if connect:
            agent = self._agents.agents_by_id[agent_id]
            ixon_vpn_client.connect(agent=agent)
            if not ixon_vpn_client.wait_for_status(wanted_status=CONNECTION_STATUS.CONNECTED):
                print("Failed to connect. exiting")
                sys.exit(0)
