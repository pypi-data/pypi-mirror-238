"""Interface with the Megatron device via http protocol."""
import json
import subprocess
import logging

from dataclasses import dataclass
import pathlib
import platform
import requests


from src.globals.helpers import __version__

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s :: %(name)s :: %(message)s :: %(levelname)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename=f"{ROOT}/mg.log",
    filemode="w",
)

logger = logging.getLogger(__name__)

BAUDRATE = 115_200
DEVICE_PORT: int = int()
PORT: str = str()


def find_device(device_number: int = DEVICE_PORT) -> tuple[str, list[str]]:
    """Find the Megatron device plugged into the Linux computer."""
    logger.debug("%s() called", find_device.__name__)

    results: list[str] = []
    win_str: str = "COM3"
    not_found: str = "Device not found"
    system: str = platform.system().lower()

    # Determine if system is Linux or WIN
    if system.lower() == "linux":
        # Search Linux filesystem for device
        find = ["find /dev -iname 'ttyACM*'"]
        try:
            logger.info(
                msg=f"{find_device.__name__} function executing\
 linux shell command to get device file names"
            )
            results_ = subprocess.run(
                check=False,
                args=find,
                shell=True,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                encoding="utf-8",
                capture_output=False,
            )
            results = sorted(results_.stdout.strip().splitlines())

            try:
                port = results[device_number]
            except IndexError:
                logger.error(not_found)
                return not_found, results

            logger.info(msg=f"Connected Devices: {results}")
            logger.debug(msg=f"Chosen Device: {port}")
            return port, results
        except IndexError:
            logger.exception(not_found)
            # print(not_found)
            return not_found, results

    elif system.lower() == "windows":
        logger.info("%s  discovered", system)

        return win_str, [win_str]

    return ("", [""])


def post_request_structure(endpoint: str, body: str):
    """Send a post request to the server."""
    logger.info("%s() called", post_request_structure.__name__)
    if "status" in endpoint or "killpower" in endpoint or "reboot" in endpoint:
        body: dict = {
            "port": body["port"].strip(),
        }
        logger.info("'if' API: body: %s", body)
    else:
        body: dict = {
            "port": body["port"].strip(),
            "channel": body["channel"],
            "value": body["value"],
        }
        logger.info("else API:: %s", body)

    logger.info("After if statement: %s", body)
    return output_post(endpoint, body)


def output_post(endpoint, body):
    """Send a post request to the API server."""
    logger.debug("%s() called", output_post.__name__)
    port = 8082
    output: dict = requests.post(
        url=f"http://localhost:{port}/{endpoint}",
        headers={
            "Content-Type": "application/json",
            "Content-Length": str(len(json.dumps({"port": body["port"]}))),
            "Host": f"localhost:{port}",
            "User-Agent": f"mgtron/{__version__}",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        },
        json=body,
        timeout=18,
    )
    logger.info("API POST Content length: %s,", len(json.dumps(body)))
    logger.info("API POST Content: %s", json.dumps(body))

    return output


def format_json(content):
    """Deserialize the incoming API data."""
    logger.debug("%s() called", format_json.__name__)

    serialed = content.decode("utf-8")
    serialed = serialed.replace('"', "")
    serialed = serialed.split("\\")

    serialed.remove("{")

    data_without_semicolons = [data.replace(':', '') for data in serialed]
    data_without_bracket = [
        data.replace('}', '')
        for data in data_without_semicolons
    ]
    result_dict = {}
    val_list = []
    key_list = []
    for _, data in enumerate(data_without_bracket):
        if data.startswith("["):
            val_list.append(data)
        else:
            key_list.append(data)
    updated_vals = [elem.rstrip(',') for elem in val_list]
    logger.debug(updated_vals)

    final_vals = []

    for _, data in enumerate(updated_vals):
        data = data.strip('[]')
        final_vals.append([str(item) for item in data.split(',')])

    logger.debug(final_vals)

    result_dict = dict(zip(key_list, final_vals))

    logger.debug("result_dict: %s", result_dict)
    return result_dict


@dataclass(slots=True)
class Megatron:
    """Class to organize the manipulation of 8 channels."""

    logger.debug(msg="\n\nGUI LAUNCHED\n\n")

    @classmethod
    def status(cls, teensy_port: str):
        """Display the status of the Teensy and return the data."""
        logger.debug("%s() called", cls.status.__name__)

        logger.debug("PORT: %s", teensy_port)

        output = post_request_structure(
            endpoint="status",
            body={
                "port": teensy_port
            }
        )

        logger.debug("OUTPUT: %s", output)
        return output

    def change_power(self, channel: int, power_level: int, teensy_port: str):
        """Change the power level of a channel Range: 0-63."""
        logger.debug("%s()", self.change_power.__name__)
        post_request_structure(
            endpoint="power",
            body={
                "port": teensy_port,
                "channel": channel,
                "value": power_level
            }
        )
        logger.info("Power level changed to %s", power_level)
        logger.info("Channel %s", channel)
        logger.info("Teensy Port: %s", teensy_port)

    def change_freq(
            self,
            channel: int,
            freq: float,
            teensy_port: str
    ) -> None:
        """Change the frequency of a channel Range: 50 - 6400 MHz."""
        logger.debug("%s()", Megatron.change_freq.__name__)
        post_request_structure(
            endpoint="freq",
            body={"port": teensy_port,
                  "channel": channel,
                  "value": float(freq)
                  }
        )

        logger.info("Frequency changed to %s", freq)
        logger.info("Channel %s", channel)
        logger.info("Teensy Port: %s", teensy_port)

    def change_bandwidth(
            self,
            channel: int,
            percentage: float,
            teensy_port: str
    ) -> None:
        """Change the bandwidth of a channel; Range: 0 - 100."""
        logger.debug("%s()", Megatron.change_bandwidth.__name__)
        post_request_structure(
            endpoint="bw",
            body={"port": teensy_port, "channel": channel,
                  "value": float(percentage)}
        )
        logger.info("Bandwidth changed to %s", percentage)
        logger.info("Channel %s", channel)
        logger.info("Teensy Port: %s", teensy_port)

    def amplification(
        self,
        channel: int,
        state: bool,
        teensy_port: str
    ) -> None:
        """Output HIGH or LOW logic level out of a chosen channel."""
        logger.debug("%s()", Megatron.amplification.__name__)
        post_request_structure(
            "amplify",
            {"port": teensy_port, "channel": channel, "state": state}
        )
        logger.debug("port %s, channel %s, state %s set",
                     teensy_port, channel, state)

    def reset_board(self, teensy_port: str) -> None:
        """Reset the power of the board."""
        logger.debug("%s()", Megatron.reset_board.__name__)
        post_request_structure(
            endpoint="killpower",
            body={"port": teensy_port}
        )
        logger.debug("port %s reset", teensy_port)

    def reboot_board(self, teensy_port: str):
        """Reboots the board."""
        logger.debug("%s()", Megatron.reboot_board.__name__)

        post_request_structure(
            endpoint="reboot",
            body={"port": teensy_port}
        )

        logger.debug("port %s rebooted", teensy_port)

    logger.info(msg="class Megatron initialized")


logger.debug(msg=f"EOF: {__name__}")


def main() -> None:
    """To Executed directly."""
    # import random

    # find_device("linux")
    # test_1 = Megatron()

    # for i in range(8):
    # test_1.change_power(i+1, random.randint(a=10, b=63))
    # sleep(1)
    # test_1.change_freq(i+1, random.randint(a=50, b=6300))
    # sleep(1)
    # test_1.change_bandwidth(i+1, random.randint(a=10, b=100))
    # sleep(1)
    # sleep(1)
    # test_1.reset_board()

    # test_1.change_freq(1, 2545.54)
    # test_1.change_power(1, 63)

    # test_1.status(PORT=PORT)
    # print("\n", format_output())

    # test_1.amplification(3, True)
    # test_1.stability(True)
    # test_1.save_state(True)


if __name__ == "__main__":
    main()
