"""Make remote API calls to find Bluetooth device names."""


from src.globals.helpers import BLE_BTNS_LIST
from src.globals.helpers import enable_select_btns
from src.globals.helpers import disble_select_btns

from src.ble.ble_data import threaded_ble_scan


from src.db.models import clear_ble_table

# from src.gui.helpers import no_power

import dearpygui.dearpygui as dpg
from decouple import config
from datetime import datetime
from typing import Callable

import time
import logging
import requests
import tabulate

tabulate.PRESERVE_WHITESPACE = True


loggei = logging.getLogger(name=__name__)


# Blue Button Theme
with dpg.theme() as blue_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))  # BLUE
# Orange Button Theme
with dpg.theme() as orng_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 165, 0, 255))  # ORANGE


def get_device_name(mac: str) -> dict:
    """Make the remote API call to get the device name."""
    api_key: str = config("API_KEY")

    url = "https://mac-address-lookup1.p.rapidapi.com/static_rapid/mac_lookup/"

    # print(f"mac: {mac}")
    querystring = {"query": mac}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "mac-address-lookup1.p.rapidapi.com",
    }

    response = requests.get(
        url,
        headers=headers,
        params=querystring,
        timeout=23,
    )

    # print(json.dumps(response.json(), indent=4))

    return response.json()


def bluetooth_scan_jam(sender) -> None:
    """Scan the local bluetooth channels and jam them."""
    loggei.info(msg="BLE method called")

    # Information relevant to toggling between the ble and wifi scan
    loggei.info(f"dpg wifi item value = {dpg.get_item_theme(item='mssn_scan_jam')}")

    # If wifi button is orange, execute the following
    if dpg.get_item_theme(item="mssn_scan_jam") == 39:
        loggei.debug("WiFi orange button conditonal triggered")
        loggei.debug("Changing WiFi button to blue")
        dpg.bind_item_theme(
            item="mssn_scan_jam",
            theme=blue_btn_theme,  # WTF Only hard-coding the color works; Blue
        )
        loggei.debug("WiFi button changed to blue")
        loggei.debug(
            f"dpg wifi item value = {dpg.get_item_theme(item='mssn_scan_jam')}"
        )
        # loggei.debug(msg="WiFi scan button disabled")

        try:
            # Delete the open WiFi scan window
            dpg.configure_item(item=129, show=False, modal=False)
            dpg.configure_item(item="128", show=False, modal=False)
            loggei.debug(msg="WiFi scan window configured to delete")

            # Makes no sense why configure first is needed to delete
            dpg.delete_item(item=129)
            dpg.delete_item(item="128")
            loggei.debug(msg="WiFi scan window relative items deleted")

            dpg.delete_item(item="wifi_scan_window")

            loggei.debug(msg="WiFi scan window deleted")
        except (SystemError, FileNotFoundError) as err:
            loggei.warning("WiFi scan btn: %s", err)
        finally:
            loggei.debug("Re-enabling the WiFi scan button")
            wifi = ["mssn_scan_jam"]
            enable_select_btns(*wifi, _dpg=dpg)

    # Disable the buttons that should not be used during the scan
    disble_select_btns(*BLE_BTNS_LIST, _dpg=dpg)

    try:
        # Conditional lgic to determine if the scan is in progress
        if dpg.get_item_theme(item=sender) == orng_btn_theme:
            dpg.bind_item_theme(
                item="mssn_bluetooth_scan",
                theme=blue_btn_theme,
            )

            dpg.configure_item(
                item=sender,
                label=" TRACKER \n   TAG",
            )
            loggei.debug(msg="Bluetooth scan button disabled")

            # Delete the open ble scan window
            dpg.delete_item(item="12")
            loggei.debug(msg="Bluetooth scan window deleted")

            # Re-enable the buttons that were disabled
            enable_select_btns(*BLE_BTNS_LIST, _dpg=dpg)

        else:
            # Delete the old contents of the DB
            clear_ble_table()

            # Launch the window that will show the bluetooth information
            dpg.bind_item_theme(
                item=sender,
                theme=orng_btn_theme,
            )
            dpg.configure_item(
                item=sender,
                label=" TRACKER \n   TAG",
            )
            loggei.debug(msg="Bluetooth scan button enabled")

            with dpg.window(
                tag="12",
                no_scrollbar=True,
                no_collapse=True,
                no_resize=True,
                no_title_bar=True,
                no_move=True,
                pos=(0, 0),
                width=880,
                height=720,
            ):
                with dpg.child_window(
                    tag="ble_labels",
                    pos=(0, 0),
                    width=880,
                    height=55,
                ):
                    dpg.add_text(
                        default_value=" " * 7
                        + "MAC"
                        + " " * 10
                        + "|"
                        + " " * 3
                        + "MANUFACTURER"
                        + " " * 3
                        + "|"
                        + " "
                        + "RSSI"
                        + " "
                        + "|"
                        + " " * 2
                        + "TIME"
                        + " " * 2
                        + "|"
                        + " "
                        + "DISTANCE"
                        + " " * 2
                        + "|"
                        + " "
                        + "LOCATION",
                        label="BLUETOOTH LIST",
                    )

                with dpg.child_window(
                    tag="ble_list",
                    no_scrollbar=False,
                    pos=(0, 60),
                    width=880,
                    height=680,
                ):
                    # Get the BLE dict information and print to GUI
                    all_data: dict[str, list[str, str, str, str]] = threaded_ble_scan(
                        (True, False)
                    )
                    # print(f"all_data = {all_data}")

                    # Sort the dict by the the index 1 of the value
                    all_data = dict(
                        sorted(
                            all_data.items(),
                            key=lambda x: x[1][1],
                            reverse=False,
                        )
                    )

                    # text_color: list[tuple] = []

                    converted_data = []
                    for i in all_data.items():
                        # print(f"i = {i}")
                        new_list = []
                        new_list.append(i[0])
                        new_list.append(i[1][0])  # Manufacturer
                        new_list.append(i[1][1] + "dBm")  # RSSI
                        new_list.append(f" {datetime.now().strftime('%H:%M:%S')}")
                        # new_list.append(i[1][2]) # Tracker tag: bool
                        new_list.append(str(i[1][3]) + "m")  # Distance
                        new_list.append(i[1][4])  # GPS location

                        # Red if tracker tag is true, white if false
                        # text_color.append((255, 0, 0, 255) if i[1][2] == "true"
                        # else (255, 255, 255, 255))

                        converted_data.append(new_list)

                    for j, i in enumerate(converted_data):
                        # print(f"j = {j}")
                        mac_diff = 18 - len(i[1])
                        if len(i[0]) < 18:
                            i[0] += " " * mac_diff
                        dpg.add_text(
                            # tag=i[1],  # Causes issue on re-scan
                            # color=text_color[j],
                            default_value=tabulate.tabulate(
                                [i],
                                stralign="left",
                                tablefmt="plain",
                            ),
                        )
                        dpg.add_text(default_value=" ")

    except SystemError:
        loggei.error(msg="Bluetooth scan window not found")
        return

    # Re-enable the buttons that were disabled (wifi)
    loggei.debug("This is where the bluetooth window finishes opening")
    logging.debug("Re-enabling the WiFi scan button")
    wifi = ["mssn_scan_jam"]
    enable_select_btns(*wifi, _dpg=dpg)


def bluetooth_defeat(
    callstack_helper: Callable[
        [
            int,
        ],
        None,
    ]
) -> None:
    """Default BLE jamming algorithm."""
    loggei.info(msg="SCANNING...")

    try:
        dpg.delete_item(item="12")
    except SystemError:
        loggei.error(msg="Bluetooth scan window not found")
        loggei("quitting")
        return

    # Default BLE jamming algorithm
    bluetooth_blocker_init: list[tuple[int, int, int]] = [
        (2402, 100, 20),
        (2426, 100, 20),
        (2480, 100, 20),
        (2426, 0, 20),
        (2410, 100, 100),
        (2430, 100, 100),
        (2450, 100, 100),
        (2470, 100, 100),
    ]

    _ = [  # Set the values of the bluetooth frequencies
        (
            dpg.set_value(
                item=f"freq_{i}",
                value=float(vals[0]) if isinstance(vals[0], int) else 50.0,
            ),
            dpg.set_value(
                item=f"power_{i}",
                value=vals[1] if int(vals[0]) != 50 else 0,
            ),
            dpg.set_value(
                item=f"bandwidth_{i}",
                value=vals[2],
            ),
            loggei.info("Bluetooth frequency set in GUI: %s", vals),
            # Automatically send the command to the MGTron board
            callstack_helper(channel=i),
        )
        # if hardware_ids
        for i, vals in enumerate(bluetooth_blocker_init, start=1)
    ]

    seconds = 3
    loggei.info("Transmitting for %s seconds...", seconds)

    # loop for 3 seconds without sleep
    t_end = time.time() + seconds

    # Give an opportunity to stop the transmission
    while time.time() < t_end:
        if dpg.is_item_clicked(item="Stop_all_channels"):
            loggei.warning(msg="Scan jam stopper clicked")

            return

    loggei.debug("intitial ble transmission complete")
    bluetooth_blocker_post: list[tuple[int, int, int]] = [
        (2402, 100, 20),
        (2426, 100, 20),
        (2480, 100, 20),
        (2426, 0, 20),
        (2410, 0, 20),
        (2430, 0, 20),
        (2450, 0, 20),
        (2470, 0, 20),
    ]

    _ = [  # Set channels 0 thru 5 to power = 0
        (
            dpg.set_value(
                item=f"freq_{i}",
                value=float(vals[0]) if isinstance(vals[0], int) else 50.0,
            ),
            dpg.set_value(
                item=f"power_{i}",
                value=vals[1] if int(vals[0]) != 50 else 0,
            ),
            dpg.set_value(
                item=f"bandwidth_{i}",
                value=vals[2],
            ),
            loggei.debug("Bluetooth frequency set in GUI: %s", vals),
            # Automatically send the command to the MGTron board
            callstack_helper(channel=i),
        )
        # if hardware_ids
        for i, vals in enumerate(bluetooth_blocker_post, start=1)
    ]

    # Not sure if the code down here is being used

    # Set the bluetooth button to be blue
    dpg.bind_item_theme(item="mssn_bluetooth_scan", theme=blue_btn_theme)

    try:
        dpg.delete_item(item="12")
    except SystemError:
        loggei.error(msg="Bluetooth scan window not found")

    loggei.info(msg="Bluetooth yam complete")
