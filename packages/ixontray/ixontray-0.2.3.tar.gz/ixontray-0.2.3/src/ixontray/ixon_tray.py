#!/usr/bin/env python3
import argparse
import functools
import logging
import os
import signal
import sys
import time
from argparse import RawTextHelpFormatter
from typing import Any

import requests
import urllib3
from PyQt6.QtCore import QEvent, QThread, QTimer
from PyQt6.QtGui import QAction, QCloseEvent, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QMessageBox, QSystemTrayIcon

import ixontray
from ixontray.base_model_store import BaseModelStore
from ixontray.config import (
    AGENTS_FILE_PATH,
    COMMAND_FILE_NAME,
    COMMAND_FILE_PATH,
    INSTALL_DIR,
    qsettings,
)
from ixontray.ixon_cloud_api import IxonCloudAPIv1, IxonCloudAPIv2
from ixontray.ixon_vpn_client_api import CONNECTION_STATUS, IxonVpnClient
from ixontray.launcher import Launcher
from ixontray.settings_window import SettingsWindow
from ixontray.telemetry import log_telemetry, telemetry
from ixontray.types.api import Agent, IXapiApplicationID, Server
from ixontray.types.common import AgentList, Command, Commands
from ixontray.update import update_available

urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IXON_TRAY")
logger.setLevel(logging.DEBUG)


class IxonTray:
    CONNECT_TIMEOUT = 60

    def _get_status_from_ixon_vpn_client(self) -> None:
        if self._ixon_vpn_client:
            try:
                self._ixon_status = self._ixon_vpn_client.status()
                if self._ixon_status["status"] == "error":
                    msg = (
                        "It looks like your local IXON client is not running"
                        " please make sure your local client runs and try again"
                        " or download it from the IXON website"
                    )
                    self.tray.showMessage(
                        "IXON tray",
                        msg,
                    )
            except requests.exceptions.ConnectionError:
                msg = QMessageBox()
                msg.setText(
                    (
                        "Ixon client could not connect to the ixon vpn client. Please visit: <a"
                        ' href="https://support.ixon.cloud/hc/en-us/articles/360014815979-VPN-client-installation-and-uninstallation">Installation'
                        " instructions</a>for instructions on how to install the vpn client and restart the"
                        " application."
                    ),
                )
                msg.setWindowTitle("Ixon vpn client missing")

                msg.exec()

    @log_telemetry
    def get_agents(self) -> dict[str, Agent]:
        ixon_ids = {}
        # API v1
        res1 = self._ixon_api_v1.get_companies()
        if res1 is None:
            self.tray.showMessage("IXON tray", "Failed to connect, please check your login details")
            self.show_login_credentials()
            return {}
        logger.info("Loaded agent list from cloud v1.")
        companies = [(c, self._ixon_api_v1) for c in res1.data]
        res2 = self._ixon_api_v2.get_companies()
        if res2 is None:
            self.tray.showMessage("IXON tray", "Failed to connect, please check your login details")
            self.show_login_credentials()
            return {}
        logger.info("Loaded agent list from cloud v2.")
        companies += [(c, self._ixon_api_v2) for c in res2.data]

        if companies is None:
            self.tray.showMessage("IXON tray", "Failed to connect, please check your login details")
            return {}

        for company, api in companies:
            logger.info(f"Loading agents for  {company.name} / {company.publicId}")
            agents = None
            agents = api.get_agents(company_id=company.publicId)
            if agents is None:
                continue
            for a in agents.data:
                a.company_id = company.publicId
                a.api_version = api.VERSION
                ixon_ids[a.publicId] = a

        return ixon_ids

    @log_telemetry
    def run_command(self, *_: Any, command: Command, ixon_id: str | None = None) -> None:
        logger.info(f"Running: {command}")

        if command.force_connection:
            logger.info("This command requires a connection connecting")
            if ixon_id is None and not self._ixon_vpn_client.connected():
                logger.warning("Not connected, please connect first")
                return

            if ixon_id is None:
                ixon_id = self._ixon_status["agentId"]

            self.connect_to_ixon(ixon_id=ixon_id)
            logger.info("Connected")

        logger.info("Running actual command")
        command.execute()

    @log_telemetry
    def connect_to_ixon(self, ixon_id: str) -> None:
        # Connect to IXONi

        self._ixon_status = self._ixon_vpn_client.status()
        disconnected = False
        logger.info(f"Current status: {self._ixon_status}")

        # if we are here and still connected we are connected ot the right system
        if self._ixon_vpn_client.connected() and ixon_id in self._ixon_status.get("agentId", ""):
            logger.info("Already connected")
            return

        if self._ixon_vpn_client.connected():
            self.tray.showMessage("IXON tray", "Disconnecting from previous host.")
            logger.info(f"Disconnecting from previous host: {self._ixon_status}")
            self._ixon_vpn_client.disconnect()
            disconnected = True
            logger.info("Wait for disconnect")
            self._ixon_vpn_client.wait_for_status(wanted_status=CONNECTION_STATUS.IDLE)
            logger.info("Disconnected")

        msg = f"Connecting to {self._agents_list.agents_by_id[ixon_id]}"
        self.tray.showMessage("IXON tray", msg)
        logger.info(msg)

        if self._ixon_status["data"] == "idle" or disconnected:
            max_tries = 3
            for i in range(max_tries):
                if self._ixon_vpn_client.connect(agent=self._agents_list.agents_by_id[ixon_id]):
                    break
                logger.info(f"You have {max_tries - i - 1} tries left.")

        self._ixon_status = self._ixon_vpn_client.status()

        if not self._ixon_vpn_client.wait_for_status(
            wanted_status=CONNECTION_STATUS.CONNECTED,
            timeout=self.CONNECT_TIMEOUT,
        ):
            msg = "Failed to connect, please check your login details"
            self.tray.showMessage("IXON tray", msg)
            logger.info(msg)
        else:
            msg = "Connected"
            logger.info(msg)
            self.tray.showMessage("IXON tray", msg)
            self.setup_menu()

    @log_telemetry
    def save_commands_cb(self, commands: Commands) -> None:
        """Save the updated commands."""
        self._command_store.save(commands)
        self._commands = self._command_store.load()
        self.setup_menu()

    def _has_login_details(self) -> bool:
        """Check if login details are there."""
        return all(self._settings_window.general_tab.get_auth())

    def get_auth_string(self, otp: str = "") -> str:
        email, password = self._settings_window.general_tab.get_auth()

        if not email or not password:
            logger.error("No login details found please supply them")
            self.show_login_credentials()
            return ""

        return IxonCloudAPIv1.generate_auth(email=email, pwd=password, otp=otp)

    def show_login_credentials(self) -> None:
        self._settings_window.show()
        self._settings_window.setCurrentIndex(0)

    def _setup_ixon_apis(self) -> None:
        logger.info("Setting up apis")
        auth_string = self.get_auth_string()
        if auth_string is None:
            logger.info("No auth string")
            return
        self._ixon_api_v1 = IxonCloudAPIv1(application_id=IXapiApplicationID)
        token = self._ixon_api_v1.generate_access_token(auth=auth_string)
        if token is not None:
            self._ixon_vpn_client = IxonVpnClient(token=token)
            self._ixon_api_v2 = IxonCloudAPIv2(application_id=IXapiApplicationID, token=token)
        else:
            self.show_login_credentials()

    def __init__(self) -> None:
        self.update = None
        self.menu = QMenu()

        self.favourite_ixon_ids: dict[str, Agent] = {}

        self.current_item_menu = []

        self._agent_store = BaseModelStore[AgentList](file_path=AGENTS_FILE_PATH, empty_if_not_valid=True)
        self._agents_list = self._agent_store.load()

        self._command_store = BaseModelStore[Commands](
            file_path=COMMAND_FILE_PATH,
            default_path=INSTALL_DIR / COMMAND_FILE_NAME,
        )
        self._commands = self._command_store.load()

        self.connected_icon = QIcon(os.path.join(INSTALL_DIR, "icon.png"))
        self.disconnected_icon = QIcon(os.path.join(INSTALL_DIR, "icon_not_connected.png"))

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(os.path.join(INSTALL_DIR, "icon_not_connected.png")))
        self.tray.setVisible(True)

        # Setting up persistent settings
        self._settings = qsettings
        self._settings_window = SettingsWindow(settings=self._settings)

        self._ixon_api_v1: None | IxonCloudAPIv1 = None
        self._ixon_vpn_client = None
        self._setup_ixon_apis()

        self._ixon_status = {}
        self._get_status_from_ixon_vpn_client()

        self._settings_window.closeEvent = self.update_settings
        self._settings_window.commands_tab.commands_updated.connect(self.save_commands_cb)

        self._settings_window.commands_tab.set_commands(self._commands)
        # self._settings_window.show()

        self.load_favourite_ixon_ids()
        self._settings_window.clients_tab.set_all_clients(self._agents_list.agents_by_id, self.favourite_ixon_ids)

        # Creating the options
        self.setup_menu()

        self.tray.show()

        self._worker_thread = QThread()
        self._worker_thread.start()
        self._update_status_timer = QTimer()
        self._update_agents_timer = QTimer()

        # Update status every 1 seconds
        self._update_status_timer.timeout.connect(self.update_status)
        self._update_status_timer.start(1000 * 1)
        self._update_status_timer.moveToThread(self._worker_thread)

        # Update agents every 10m seconds
        self.update_agents()
        self._update_agents_timer.timeout.connect(self.update_agents)
        self._update_agents_timer.start(1000 * 60 * 5)
        self._update_agents_timer.moveToThread(self._worker_thread)

        if not self.get_auth_string():
            logger.info("Please provide login credentials")

        logger.info("Started application, use tray icon to interact")
        telemetry.send()

    def load_favourite_ixon_ids(self) -> None:
        self._settings.beginGroup("favourite_clients")
        keys = self._settings.allKeys()
        if self._agents_list.agents_by_id:
            self.favourite_ixon_ids = {
                k: self._agents_list.agents_by_id[k] for k in keys if k in self._agents_list.agents_by_id
            }
        else:
            self.favourite_ixon_ids = {}
        self._settings.endGroup()

    def save_favourite_ixon_ids(self, favourite_ixon_ids: dict[str, str]) -> None:
        self._settings.beginGroup("favourite_clients")
        self._settings.remove("")
        for client_name, client_id in favourite_ixon_ids.items():
            logger.info(f"Saveing the following clients: {client_id}:{client_name}")
            self._settings.setValue(f"{client_name}", client_id)
        self._settings.endGroup()

    def setup_menu(self) -> None:
        self.menu.clear()

        self.connection_status = self.menu.addAction("Not Connected")
        self.menu.addAction(self.connection_status)
        self.menu.addSeparator()

        # Add entries for the current connected client
        self.add_menu_items_for_connected_client(self.menu)
        self.menu.addSeparator()
        self.add_global_menu_items(self.menu)

        self.menu.addSeparator()

        self.add_menu_items_for_favourites(self.menu)

        self.menu.addSeparator()
        #
        self.add_menu_items_for_all_clients(self.menu)

        self.menu.addSeparator()
        # To disconnect
        self.open_settings_action = QAction("Configuration")
        self.open_settings_action.setIcon(QIcon.fromTheme("application-self.menu-symbolic"))
        self.open_settings_action.triggered.connect(self.open_settings)
        self.menu.addAction(self.open_settings_action)
        # To disconnect
        self.disconnect = QAction("Disconnect VPN")
        self.disconnect.setIcon(QIcon.fromTheme("network-vpn-disconnected-symbolic"))
        self.disconnect.triggered.connect(self.disconnect_from_ixon)
        self.menu.addAction(self.disconnect)
        # To quit the app
        self.quit = QAction("Quit")
        self.quit.setIcon(QIcon.fromTheme("application-exit-symbolic"))
        self.quit.triggered.connect(app.quit)
        self.menu.addAction(self.quit)

        update, version = update_available()

        if update:
            self.menu.addSeparator()
            self.update = QAction(f"Update to {version} available.")
            self.update.setIcon(QIcon.fromTheme("dialog-warning"))
            self.menu.addAction(self.update)

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.show_menu)
        self.tray.setToolTip("Ixontray")

    def add_menu_items_for_all_clients(self, menu: QMenu) -> None:
        sub_menu = menu.addMenu("All other clients")
        for ixon_id, agent in self._agents_list.agents_by_id.items():
            connect = sub_menu.addAction(agent.full_name)
            connect.triggered.connect(lambda _, ixon_id=ixon_id: self.connect_to_ixon(ixon_id=ixon_id))
            if agent.online:
                connect.setIcon(QIcon.fromTheme("emblem-default"))
            else:
                connect.setIcon(QIcon.fromTheme("emblem-unreadable"))

    def add_menu_items_for_favourites(self, menu: QMenu) -> None:
        for ixon_id, agent in self.favourite_ixon_ids.items():
            sub_menu = menu.addMenu(agent.full_name)

            # Add default
            connect = sub_menu.addAction("Connect VPN")
            if self._agents_list.agents_by_id[ixon_id].online:
                connect.setIcon(QIcon.fromTheme("network-vpn-symbolic"))
                connect.setToolTip("Click to connect")
            else:
                sub_menu.setIcon(QIcon.fromTheme("emblem-unreadable"))
                connect.setIcon(QIcon.fromTheme("emblem-unreadable"))
                connect.setToolTip("Client is not reachable")

            connect.triggered.connect(lambda _, ixon_id=ixon_id: self.connect_to_ixon(ixon_id=ixon_id))

            for cmd in self._commands.commands:
                if "item" in cmd.show_in:
                    menu_action = sub_menu.addAction(f"Connect and {cmd.name}")
                    menu_action.setIcon(QIcon.fromTheme(cmd.icon))
                    menu_action.triggered.connect(functools.partial(self.run_command, command=cmd, ixon_id=ixon_id))

            # Add a sub menu for all defined servers
            self.menu.addSeparator()
            self.add_server_menu(agent, ixon_id, sub_menu)

    def add_server_menu(self, agent: Agent, ixon_id: str, menu: QMenu) -> QMenu:
        sub_menu = menu.addMenu("IXON defined servers (Beta)")
        for server in agent.servers:
            menu_action = sub_menu.addAction(server.name)
            menu_action.triggered.connect(
                functools.partial(self.run_server_command, agent=agent, ixon_id=ixon_id, server=server),
            )
        return sub_menu

    def run_server_command(self, agent: Agent, server: Server, ixon_id: str) -> None:
        if agent.api_version == 1:
            url = self._ixon_api_v1.get_webaccess_url_from_server(agent, server)
        else:
            url = self._ixon_api_v2.get_webaccess_url_from_server(agent, server)

        if url:
            xdg_open_command = Command(
                name=f"XDG_open {server.name}",
                icon="web-browser-symbolic",
                cmd=f"xdg-open {url}",
                force_connection=False,
            )

            self.run_command(command=xdg_open_command, ixon_id=ixon_id)

    def add_global_menu_items(self, menu: QMenu) -> None:
        for cmd in self._commands.commands:
            if "global" in cmd.show_in:
                menu_action = menu.addAction(cmd.name)
                menu_action.setIcon(QIcon.fromTheme(cmd.icon))
                menu_action.triggered.connect(functools.partial(self.run_command, command=cmd))

    def add_menu_items_for_connected_client(self, menu: QMenu) -> None:
        self.current_item_menu = []
        for cmd in self._commands.commands:
            if "item" in cmd.show_in:
                self.current_item_menu.append(menu.addAction(f"{cmd.name}"))
                self.current_item_menu[-1].setIcon(QIcon.fromTheme(cmd.icon))
                self.current_item_menu[-1].triggered.connect(functools.partial(self.run_command, command=cmd))

        # Add a sub menu for all defined servers
        self.menu.addSeparator()
        ixon_id = self._ixon_status.get("agentId", None)
        if ixon_id:
            agent = self._agents_list.agents_by_id[ixon_id]
            self.current_item_menu.append(self.add_server_menu(agent, ixon_id, menu))

    def disconnect_from_ixon(self) -> None:
        self.tray.showMessage("IXON tray", "Disconnecting")
        logger.info("Disconnecting...")
        self._ixon_vpn_client.disconnect()

    def show_menu(self, _: QEvent) -> None:
        self.menu.show()

    def update_settings(self, _: QCloseEvent) -> None:
        self._setup_ixon_apis()

        if self._ixon_api_v1 is not None and self._ixon_api_v1.has_valid_token():
            fav_ixon_ids = self._settings_window.clients_tab.get_favourite_ixon_ids()
            self.save_favourite_ixon_ids(fav_ixon_ids)
            self.load_favourite_ixon_ids()
            self._settings_window.commands_tab.set_commands(self._commands)
            self.setup_menu()
            #
        QTimer.singleShot(100, self.update_agents)

    def update_agents(self) -> None:
        logger.info("Updating Agent info.")
        if self._ixon_api_v1 is not None and self._ixon_api_v1.has_valid_token():
            # Refresh auth token
            self._setup_ixon_apis()
            # Update agents
            self._agents_list.agents_by_id = self.get_agents()
            self._settings_window.clients_tab.set_all_clients(
                clients=self._agents_list.agents_by_id,
                favourites=self.favourite_ixon_ids,
            )
            self._agent_store.save(self._agents_list)
            self.setup_menu()
        else:
            self.show_login_credentials()

        telemetry.send()

    @log_telemetry
    def open_settings(self, _: bool = False) -> None:
        logger.info("Opening settings window")
        self._settings_window.show()

    @log_telemetry
    def update_status(self, _: bool = False) -> None:
        if self._ixon_api_v1 is not None and self._ixon_api_v1.has_valid_token():
            self._get_status_from_ixon_vpn_client()
            logging.debug(self._ixon_status)

            if self._ixon_vpn_client.connected():
                ixon_id = self._ixon_status["agentId"]

                if ixon_id in self._agents_list.agents_by_id:
                    self.connection_status.setText(f"Connected to: {self._agents_list.agents_by_id[ixon_id].full_name}")

                self.tray.setIcon(self.connected_icon)
                for i in self.current_item_menu:
                    i.setEnabled(True)
            elif self._ixon_status.get("data", "") == CONNECTION_STATUS.CONNECTING:
                if self.tray.icon() == self.disconnected_icon:
                    self.tray.setIcon(self.connected_icon)
                else:
                    self.tray.setIcon(self.disconnected_icon)
            else:
                self.connection_status.setText("Not connected")
                self.tray.setIcon(self.disconnected_icon)
                for i in self.current_item_menu:
                    i.setEnabled(False)

    def _get_company_id_for(self, ixon_id: str) -> str:
        return self._agents_list.agents_by_id[ixon_id].company_id


app = QApplication(sys.argv)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="""
    This program lets you easily connect to an ixon host and optionally execute an commands.

    There are two ways to interact with the program.

      1. Through the ixontray icon, launched by running ixontray without arguments
      2. Through the ixontray --launcher ran by running ixontray --launcher.

    Trouble shooting:
        If the program crashes at startup try installing:
        ----------------------------------------------------------------------------------------------------------------
        $sudo apt-get -qq install libegl1 libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0
            libxcb-render-util0 libxcb-shape0 libxkbcommon-x11-0
        ----------------------------------------------------------------------------------------------------------------

    """,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "--launcher",
        "-l",
        action="store_true",
        default=False,
        help="Launch the launcher not the tray icon.",
    )
    parser.add_argument(
        "--auto-update",
        "-u",
        action="store_true",
        default=False,
        help="Update ixontray",
    )

    try:
        update, version = update_available()
        if update:
            print("#" * 60)
            print(f"Update available to {version} you are on {ixontray.__version__}, please update :-)")
            print("#" * 60)
            time.sleep(1)

        args = parser.parse_known_args()[0]

        signal.signal(signal.SIGINT, signal.SIG_DFL)

        if args.auto_update:
            print(f"auto update! {__file__}")
            os.system("pip install --upgrade ixontray --dry-run")
            sys.exit(0)

        if args.launcher:
            agent_list = BaseModelStore[AgentList](file_path=AGENTS_FILE_PATH, empty_if_not_valid=True).load()
            commands = BaseModelStore[Commands](
                file_path=COMMAND_FILE_PATH,
                default_path=INSTALL_DIR / COMMAND_FILE_NAME,
            ).load()

            launcher = Launcher(settings=qsettings)
            launcher.set_agents(agents=agent_list)
            launcher.set_commands(commands=commands)
            launcher.show()
            launcher.center()
        else:
            app.setQuitOnLastWindowClosed(False)
            IxonTray()

        code = app.exec()
        telemetry.send()
        sys.exit(code)
    except Exception as e:
        telemetry.log_crash_report()
        telemetry.send()
        raise e
