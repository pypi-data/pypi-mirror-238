"""Global helper functions for the application."""

import logging
import subprocess
import os
import threading
from decouple import config


from threading import Thread
from pathlib import Path

from dearpygui import dearpygui as dpg

# import importlib.metadata

loggi = logging.getLogger(name=__name__)

TEST: bool = bool()
BLE_BTNS_LIST: set[str] = {
    "save button",
    "quick_load",
    "custom_save",
    "custom_load_button",
    "delete_button",
    "Alpha\nConfig",
    "Bravo\nConfig",
    "Charlie\nConfig",
    "Delta\nConfig",
    "Echo\nConfig",
    "Fox\nConfig",
    "mssn_scan_jam",
    220,
    213,
}

WIFI_BTNS_LIST: set[str] = {
    "save button",
    "quick_load",
    "custom_save",
    "custom_load_button",
    "delete_button",
    "Alpha\nConfig",
    "Bravo\nConfig",
    "Charlie\nConfig",
    "Delta\nConfig",
    "Echo\nConfig",
    "Fox\nConfig",
    "mssn_bluetooth_scan",
    220,  # Load button after being pressed
    213,  # Quick load button after being pressed
}

ALL_BTNS_LIST: set[str] = {
    "save button",
    "quick_load",
    "custom_save",
    "custom_load_button",
    "delete_button",
    "Alpha\nConfig",
    "Bravo\nConfig",
    "Charlie\nConfig",
    "Delta\nConfig",
    "Echo\nConfig",
    "Fox\nConfig",
    "mssn_bluetooth_scan",
    "mssn_scan_jam",
    220,  # Load button after being pressed
    213,  # Quick load button after being pressed
}

ROOT = Path(__file__).parent.parent.parent
script_file = ROOT / "src" / "assets" / "get_latest_version.sh"


def version_getter() -> str | None:
    """Get the latest version from the CHANGELOG file."""
    # Touch the file if it doesn't exist
    # pathlib.Path(ROOT / "CHANGELOG.md").touch()
    with open(ROOT / "src" / "assets" / "CHANGELOG.cpy", encoding="utf-8") as file:
        for line in file:
            if "##" in line and "YEAR MONTH DAY" not in line:
                correct_line = line.split("-")[0].strip()
                version = correct_line.split("[")[1]

                return version.strip("]")
        return None


@DeprecationWarning
def capture_version_output(command: str) -> str:
    """Get latest version from the CHANGELOG file."""
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    return output


__version__ = version_getter()


def disble_select_btns(*btns: list[str], _dpg: dpg):
    """Disable the buttons passed into the function."""
    loggi.debug(msg=f"{disble_select_btns.__name__}()")

    for btn in btns:
        try:
            _dpg.configure_item(item=btn, enabled=False)
            loggi.info(msg=f"Button {btn} disabled")

            loggi.debug("Buttons disabled")
        except SystemError as err:
            loggi.warning("%s() | %s", disble_select_btns.__name__, err)
            loggi.warning("Buttons not disabled")

    loggi.debug("%s() complete", disble_select_btns.__name__)


def enable_select_btns(*btns: list[str], _dpg: dpg):
    """Enable the buttons passed into the function."""
    loggi.debug(msg=f"{enable_select_btns.__name__}()")

    for btn in btns:
        try:
            _dpg.configure_item(item=btn, enabled=True)
            loggi.info(msg=f"Button {btn} enabled")

            loggi.debug("%s enabled", btn)
        except SystemError as err:
            loggi.warning("%s not enabled", btn)
            loggi.warning("%s() | %s", enable_select_btns.__name__, err)

    loggi.debug("%s() complete", enable_select_btns.__name__)


class ThreadWithReturnValue(Thread):
    """Create a thread that returns a value."""

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        """Initialize the thread."""
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        """Run the thread."""
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        """Join the thread."""
        Thread.join(self, *args)
        return self._return


def launch_api_server(path: str, the_pass: str | None = None) -> None:
    """Launch the rust WiFi server."""
    loggi.debug(msg=f"{launch_api_server.__name__}()")
    loggi.info(msg=f"Path: {path}")

    if "wifi" in path:
        print("Launching WiFi server")

        command = path

        cmd1 = subprocess.Popen(["echo", the_pass], stdout=subprocess.PIPE)
        cmd2 = subprocess.Popen(
            ["sudo", "-S"] + [command] + ["&>/dev/null"],
            stdin=cmd1.stdout,
            stdout=subprocess.PIPE,
        )
        cmd2.stdout.close()

    else:

        server = str(path)

        # Launch the API server as a daemon
        pid = os.system(server)

        if pid != 0:
            loggi.warning(msg=f"API server is likely running: {server}")
            return

        loggi.info("%s server launched", server)


# BlueIO API
start_server = threading.Thread(
    target=launch_api_server,
    args=(f"{ROOT}/src/assets/blueio_rs",),
)
start_server.daemon = True
start_server.start()

root = config("DEV_PASS")

# WiFi API; sudo required
start_server = threading.Thread(
    target=launch_api_server,
    args=(
        f"{ROOT}/src/assets/wifi_rs",
        root,
    ),
)
start_server.daemon = True
start_server.start()

# MGTRON API
start_server = threading.Thread(
    target=launch_api_server,
    args=(f"{ROOT}/src/assets/api_rs",),
)
start_server.daemon = True
start_server.start()

# GPS API is locally installed via PyPi
start_server = threading.Thread(
    target=launch_api_server,
    args=("gps",),
)
start_server.daemon = True
start_server.start()


def main():
    """Run the module."""
    print(f"Version: {__version__}")


if __name__ == "__main__":
    main()
