import datetime
import http
import logging
import traceback
from collections.abc import Callable
from typing import Any
from uuid import uuid4

import pydantic
import requests

from ixontray.config import qsettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("TELEMETRY")
logger.setLevel(logging.DEBUG)


instance_id = qsettings.value("instance_id", None)
if instance_id is None:
    instance_id = str(uuid4())
    qsettings.setValue("instance_id", instance_id)


class FunctionCall(pydantic.BaseModel):
    name: str
    call_count: int = 1

    def __add__(self, other: "FunctionCall") -> "FunctionCall":
        """Add the call count of the one to the other."""
        self.call_count += other.call_count
        return self


class Report(pydantic.BaseModel):
    application: str
    instance_id: str
    run_id: str = pydantic.Field(default_factory=lambda: str(uuid4()))
    last_update: datetime.datetime
    call_count: dict[str, FunctionCall] = pydantic.Field(default_factory=dict)
    crash_report: str = pydantic.Field(default_factory=list)


def log_telemetry(func: Callable) -> Callable:
    def logged_function(*args: Any, **kwargs: Any) -> Callable:
        telemetry.log(function_call=FunctionCall(name=func.__name__))
        return func(*args, **kwargs)

    return logged_function


class Telemetry:
    def __init__(self, url: str, instance_id: str, token: str) -> None:
        self._timeout = 1
        self._url = url
        self._token = token
        self._instance_id = instance_id
        self._report = Report(application="ixontray", instance_id=instance_id, last_update=datetime.datetime.now())

    def log(self, function_call: FunctionCall) -> None:
        """Log function call."""
        self._report.last_update = datetime.datetime.now()
        if function_call.name not in self._report.call_count:
            self._report.call_count[function_call.name] = function_call
        else:
            self._report.call_count[function_call.name] += function_call

    def log_crash_report(self) -> None:
        """Add crash report."""
        self._report.crash_report = str(traceback.format_exc())

    def send(self) -> bool:
        """Send data to remote."""
        logging.debug(f"Sending update to: {self._url}")
        self._report.model_dump_json()
        try:
            res = requests.post(
                url=f"{self._url}/{self._instance_id}",
                verify=False,
                data=self._report.model_dump_json(),
                timeout=self._timeout,
            )
            print(res.text)

            return res.status_code == http.HTTPStatus.OK
        except Exception as e:
            print(e)
            return False


# telemetry = Telemetry(url="https://telemetry.mmoerdijk.nl", instance_id="mart_app", token="test_token")
telemetry = Telemetry(
    url="https://telemetry.mmoerdijk.nl",
    instance_id=str(instance_id),
    token="ea0dc150-1d13-4d8d-b139-62a5bfde2839",
)


if __name__ == "__main__":
    telemetry.log(function_call=FunctionCall(name="test_func"))
    telemetry.send()
    telemetry.log(function_call=FunctionCall(name="test_func_2"))
    telemetry.send()
