"""Helper functions for wifi business of the GUI."""

import logging
from typing import Callable
from pynput.mouse import Controller
import time
import mouse

import dearpygui.dearpygui as dpg

import tabulate

from src.globals.helpers import WIFI_BTNS_LIST
from src.globals.helpers import enable_select_btns
from src.globals.helpers import disble_select_btns

from src.wifi.scanning import post_ssid
from src.wifi.scanning import freqs_and_sigs
from src.wifi.scanning import threaded_scan
from src.wifi.scanning import find_signals_and_frequencies

from src.gui.helpers import return_teensy
from src.gui.helpers import device_refresh
from src.gui.helpers import device_names

from src.gui.interface import Megatron

from src.globals.helpers import ThreadWithReturnValue

from src.db.helpers import wifi_save
from src.db.helpers import wifi_load
from src.db.helpers import get_sort_order
from src.db.helpers import set_sort_order

from src.db.models import clear_wifi_table

from colorama import Fore as F

R = F.RESET

tabulate.PRESERVE_WHITESPACE = True

loggei = logging.getLogger(name=__name__)


# Blue Button Theme
with dpg.theme() as blue_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))  # BLUE
# Orange Button Theme
with dpg.theme() as orng_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 165, 0, 255))  # ORANGE
# Grey Button Theme
with dpg.theme() as grey_btn_theme, dpg.theme_component(dpg.mvAll):  # GREY
    dpg.add_theme_color(dpg.mvThemeCol_Button, ("128", "128", "128", 255))
# Red Button Theme
with dpg.theme() as red_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # RED


def convert_data(data):
    """Convert the data from a list of dictionaries to a list of lists."""
    loggei.debug("%s()", convert_data.__name__)

    if not data:
        return []
    keys = list(data[0].keys())
    result = []
    scan_results = []
    # Order the keys
    keys = ["ssid", "bssid", "channel", "frequency", "signal", "last_seen"]

    for dictionary in data:
        if dictionary["ssid"] == " ":
            dictionary["ssid"] = " HIDDEN SSID"

        values = [dictionary[key] for key in keys]
        result.append(values)

        # Prepare the data for the DB
        scan_results.append(
            [
                dictionary["ssid"],  # SSID
                dictionary["bssid"],  # BSSID
                int(dictionary["channel"]) if dictionary["channel"] else 0,  # Channel
                float(dictionary["frequency"]),  # Frequency
                float(dictionary["signal"]),  # Signal
                int(dictionary["last_seen"]),  # Last Seen
            ]
        )

    # Pretty print the wifi scan results for debugging and development
    # print(f"{F.YELLOW}{tabulate.tabulate(result, headers=keys)}{R}")

    # Save the wifi scan data to the DB
    wifi_save(scan_data=scan_results)

    return result


def wifi_scan_jam(sender) -> None:
    """Scan the local wifi channels and jam them."""
    loggei.info(msg="Scan jammer method called")

    disble_select_btns(*WIFI_BTNS_LIST, _dpg=dpg)
    #  Determine if the scan is in progress; toggle button

    # Bluetooth item value
    loggei.info(
        "bluetooth item value = " f"{dpg.get_item_theme(item='mssn_bluetooth_scan')}"
    )
    # If bluetooth button is orange, execute the following
    if dpg.get_item_theme(item="mssn_bluetooth_scan") == 51:
        loggei.debug("Bluetooth scan button is orange")
        loggei.debug("Orange Bluetooth conditional triggered")
        dpg.bind_item_theme(
            item="mssn_bluetooth_scan",
            theme=blue_btn_theme,
        )
        loggei.debug(msg="BLE scan button disabled")
        try:
            # Delete the open BLE scan window
            dpg.configure_item(item="12", show=False, modal=False)
            loggei.debug("BLE scan window configured for deletion")

            # Makes no sense why configure first is needed to delete
            dpg.delete_item(item="12")
            loggei.debug(msg="BLE scan window deleted")

        except (SystemError, FileNotFoundError) as err:
            loggei.warning("BLE scan btn: %s", err)
        finally:
            loggei.debug("Enabling BLE button again")
            ble = ["mssn_bluetooth_scan"]
            enable_select_btns(*ble, _dpg=dpg)

    if dpg.get_item_theme(item=sender) == orng_btn_theme:
        dpg.bind_item_theme(
            item="mssn_scan_jam",
            theme=blue_btn_theme,
        )
        loggei.debug(msg="WiFi scan button disabled")
        try:
            # Delete the open BLE scan window
            dpg.configure_item(item=129, show=False, modal=False)
            dpg.configure_item(item="128", show=False, modal=False)

            # Makes no sense why configure first is needed to delete
            dpg.delete_item(item=129)
            dpg.delete_item(item="128")

            dpg.delete_item(item="wifi_scan_window")

            loggei.debug(msg="WiFi scan window deleted")
        except (SystemError, FileNotFoundError) as err:
            loggei.warning("WiFi scan btn: %s", err)
        finally:
            enable_select_btns(*WIFI_BTNS_LIST, _dpg=dpg)

    else:
        # Turn the button Orange
        dpg.bind_item_theme(
            item=sender,
            theme=orng_btn_theme,
        )

        scan_window()

        loggei.debug(msg="WiFi scan jammer method finished")


counter = 0


def mouse_direction() -> bool | None:
    """Determine the direction of the mouse drag."""
    loggei.info("%s()", mouse_direction.__name__)
    empty_list = []
    global counter

    while dpg.is_mouse_button_dragging(button=0, threshold=0.05):
        counter += 1
        x = dpg.get_mouse_drag_delta()
        time.sleep(0.01)
        # print(f"x: {x}")
        # print(f"count: {counter}")
        empty_list.append(x[1])
        if len(empty_list) > 4:
            if empty_list[-1] > empty_list[-2]:
                return False
            if empty_list[-1] < empty_list[-2]:
                return True
        # time.sleep(0.01)
    loggei.warning("No drag detected")
    return


def mouse_drag_callback(sender, app_data: list, user_data) -> None:
    """Scroll the window with the mouse."""
    loggei.info("%s()", mouse_drag_callback.__name__)
    # print(f"app_data: {app_data}")

    if str(app_data[2]) == "0.0":
        return

    if mouse_direction() is True:
        mouse = Controller()
        scroll_lines = -1
        mouse.scroll(0, scroll_lines)

    elif mouse_direction() is False:
        mouse = Controller()
        scroll_lines = 1
        mouse.scroll(0, scroll_lines)
    else:
        return


@DeprecationWarning
def mouse_release_callback() -> float:
    """Get the mouse drag delta."""
    drag_delta = dpg.get_mouse_drag_delta()
    # print("mouse button released")
    # print(f"drag_delta after mouse release: {drag_delta}")
    drag_delta = abs(drag_delta[1])
    return drag_delta


def scan_window() -> None:
    """Create a window to display the scan results."""
    loggei.info("%s()", scan_window.__name__)

    win_width = 880
    win_height = 675

    with dpg.window(
        tag=129,
        no_scrollbar=False,
        no_collapse=True,
        no_resize=True,
        no_title_bar=True,
        no_move=True,
        modal=True,
        pos=(0, 50),
        width=win_width,
        height=win_height,
    ):
        dpg.configure_item(item=129, show=False)

        # Delete the previouse scan results
        clear_wifi_table()

        # Get the WiFi dict information and print to GUI
        all_data: list[dict[str, str]] = threaded_scan(
            _dpg=dpg, linux_data=find_signals_and_frequencies
        )
        dpg.configure_item(item=129, show=True, modal=False)
        loggei.debug("This is where the scan window is created")
        loggei.debug("Enable bluetooth again")
        ble = ["mssn_bluetooth_scan"]
        enable_select_btns(*ble, _dpg=dpg)

        # all_data = convert_signal_to_rssi(all_data)

        # Converts to list of lists and save to DB
        new_data = convert_data(all_data)
        create_scan_results_table(
            scan_data=wifi_load(),
        )

        _ = [loggei.info("processed scan result: %s", i) for i in new_data]

    with dpg.window(
        tag="128",
        pos=(0, -50),
        width=win_width,
        height=win_height // 16.875,  # 40
        no_resize=True,
        no_scrollbar=True,
        no_collapse=True,
        no_title_bar=True,
        no_move=True,
    ):
        init_pos_x = 5
        init_pos_y = 55
        button_height = 40
        button_widths = [370, 175, 65, 90, 80, 90]

        headers = ["SSID", "MAC", "CH", "FREQ", "RSSI", "LAST SEEN"]

        dpg.add_button(
            tag=headers[0],
            label=headers[0],  # SSID
            width=button_widths[0],
            height=button_height,
            callback=sort_results,
            pos=(init_pos_x, init_pos_y),
        )

        dpg.add_button(
            tag=headers[1],
            label=headers[1],  # MAC
            width=button_widths[1],
            height=button_height,
            callback=sort_results,
            pos=(button_widths[0] + init_pos_x, init_pos_y),
        )

        dpg.add_button(
            tag=headers[2],
            label=headers[2],  # CH
            width=button_widths[2],
            height=button_height,
            callback=sort_results,
            pos=(button_widths[0] + button_widths[1] + init_pos_x, init_pos_y),
        )

        dpg.add_button(
            tag=headers[3],
            label=headers[3],  # FREQ
            width=button_widths[3],
            height=button_height,
            callback=sort_results,
            pos=(
                button_widths[0] + button_widths[1] + button_widths[2] + init_pos_x,
                init_pos_y,
            ),
        )

        dpg.add_button(
            tag=headers[4],
            label=headers[4],  # RSSI
            width=button_widths[4],
            height=button_height,
            callback=sort_results,
            pos=(
                button_widths[0]
                + button_widths[1]
                + button_widths[2]
                + button_widths[3]
                + init_pos_x,
                init_pos_y,
            ),
        )

        dpg.add_button(
            tag=headers[5],
            label=headers[5],  # LAST SEEN
            width=button_widths[5],
            height=button_height,
            callback=sort_results,
            pos=(
                button_widths[0]
                + button_widths[1]
                + button_widths[2]
                + button_widths[3]
                + button_widths[4]
                + init_pos_x,
                init_pos_y,
            ),
        )


@DeprecationWarning
def fill_scan_result(
    converted_data: list[list],
) -> None:
    """Fill the scan results window with the data."""
    loggei.info("%s()", fill_scan_result.__name__)

    scan_results: list = list()

    global data
    data = scan_results

    loggei.debug("Removing Scan Result Aliases")
    for i in converted_data:
        dpg.delete_item(item=i[1])  # Delete the alias so it can exist again

    for i in converted_data:
        # Assing name before to length can be calculated
        if len(i[0]) == 1:
            i[0] = "HIDDEN_SSID"

        ssid_difference = 32 - len(i[0])
        channel_diff = 4 - len(i[2])
        signal_diff = 3 - len(i[4])

        if len(i[0]) < 32:
            i[0] += " " * ssid_difference
        if len(i[2]) < 4:
            i[2] += " " * channel_diff
        if len(i[4]) < 3:
            i[4] += " " * signal_diff

        i[5] = f"{int(i[5]) / 1000:.2f} sec"

        try:
            dpg.add_button(
                tag=i[1],  # Causes issue on re-scan unless item deleted; MAC
                parent=129,
                label=tabulate.tabulate(
                    [i],
                    stralign="left",
                    tablefmt="plain",
                    maxcolwidths=[
                        None,
                        None,
                        None,
                        None,
                        None,
                        4,
                    ],
                ),
                width=880,
                height=60,
                callback=indicate_tagged_results,
                user_data=(i, i[1]),
            )

        except SystemError as err:
            loggei.error("Duplicate MAC address: %s", err)

        scan_results.append(
            [
                i[0],
                i[1].strip(),
                int(i[2].strip()) if i[2].strip() != "" else 0,
                float(i[3]) if i[3] != "" else 0.0,
                i[4].split(" ")[0].strip(),
                i[5],
            ]
        )

    wifi_save(scan_data=scan_results)


def mouse_click_handler(sender, app_data, user_data) -> None:
    """Mouse click handler to move the mouse when a wifi result is selected."""
    loggei.info("%s()", mouse_click_handler.__name__)
    loggei.debug("Mouse click handler method called")

    try:
        if dpg.is_mouse_button_dragging(button=0, threshold=0.01) == False:
            for i in data:
                tag = dpg.get_item_alias(item=i[1])
                if dpg.is_item_clicked(item=tag):
                    time.sleep(0.15)
                    loggei.debug("Mouse clicked (wifi)")
                    mouse.move(x=-885, y=0, absolute=False, duration=0.00001)
                    loggei.debug("Mouse moved (wifi)")
    except (SystemError, NameError) as error:
        loggei.debug("Mouse click handler message (wifi): %s", error)


def sort_results(sender, app_data, user_data):
    """Sort the results by the column clicked."""
    loggei.info("%s()", sort_results.__name__)

    loggei.info("Sender : %s", sender)

    scan_data = wifi_load()

    loggei.warning("Unsorted data(top 4): %s", scan_data[:4])

    order_query: bool = bool()
    # Add a row to the table that keeps state of the of order(asc, desc)
    order_query: bool = get_sort_order()

    if order_query:
        order_query = True
        set_sort_order(False)
    else:
        order_query = False
        set_sort_order(True)

    match sender:
        case "SSID":
            scan_data = sorted(
                scan_data, key=lambda x: x.get("ssid"), reverse=order_query
            )
        case "MAC":
            scan_data = sorted(
                scan_data, key=lambda x: x.get("mac"), reverse=order_query
            )
        case "CH":
            scan_data = sorted(
                scan_data, key=lambda x: x.get("channel"), reverse=order_query
            )
        case "FREQ":
            scan_data = sorted(
                scan_data,
                key=lambda x: x.get("frequency"),
                reverse=order_query,
            )
        case "RSSI":
            scan_data = sorted(
                scan_data,
                key=lambda x: x.get("signal"),
                reverse=not order_query,
            )
        case "LAST SEEN":
            scan_data = sorted(
                scan_data, key=lambda x: x.get("last_seen"), reverse=order_query
            )
        case _:
            loggei.error("Invalid sender: %s", sender)

    [loggei.warning("Sorted data(top 4): %s", i) for i in scan_data[:4]]

    # Create the table of scan results
    create_scan_results_table(scan_data=scan_data)


def create_scan_results_table(scan_data: list[dict]) -> None:
    """Create the table of scan results for when sorted."""
    loggei.debug("%s()", create_scan_results_table.__name__)

    # Delete the alias of the current scan results
    loggei.debug("Removing Scan Result Aliases")
    for i in scan_data:
        dpg.delete_item(item=i.get("mac"))  # Delete the alias

    # Iterate through the scan results (list of dicts) using the items method
    # Append MHZ and DBM to the frequency and signal values in the dict
    loggei.debug("Iterating through scan results")
    for s_data in scan_data:
        for i, data in s_data.items():
            if i == "frequency":
                loggei.debug("Frequency key found")
                s_data["frequency"] = f"{data} MHz"
                loggei.debug("Frequency value changed")
            if i == "signal":
                loggei.debug("Signal key found")
                s_data["signal"] = f"{data} dBm"
                loggei.debug("Signal value changed")
            # if i == "ssid":
            #     loggei.debug("SSID key found")
            #     s_data["ssid"] = "HIDDEN_SSID" if data == "" else data
            #     loggei.debug("SSID value changed")

        loggei.info(f"i: {s_data}")

    for i, data in enumerate(scan_data):
        ssid_difference = 32 - len(data.get("ssid"))
        channel_diff = 4 - len(str(data.get("channel")))
        signal_diff = 3 - len(str(data.get("signal")))

        if len(data.get("ssid")) < 32:
            x = str(data["ssid"])
            x += " " * ssid_difference
            data["ssid"] = x
        if len(str(data.get("channel"))) < 4:
            x = str(data["channel"])
            x += " " * channel_diff
            data["channel"] = x
        if len(str(data.get("signal"))) < 3:
            x = str(data["signal"])
            x += " " * signal_diff
            data["signal"] = x
        # if len(data.get("last_seen")) == 0:
        # data["last_seen"] = "Never"

        loggei.info("MACS: %s", i)
        loggei.info("Expecting data: %s", data)

        # Delete all the keys before making the button
        loggei.debug("Removing Scan Result Aliases")
        # Delete the alias so it can exist again

        dpg.delete_item(item=data.get("mac"))

        # print(data.get("mac", "No MAC"))

        dpg.add_button(
            parent=129,
            tag=data.get("mac"),
            label=tabulate.tabulate(
                [data],
                stralign="left",
                tablefmt="plain",
                maxcolwidths=[
                    None,
                    None,
                    None,
                    None,
                    None,
                    4,
                ],
            ),
            width=880,
            height=60,
            callback=indicate_tagged_results,
            user_data=(data, i),
        )


def indicate_tagged_results(sender, app_data, user_data: list[str]) -> None:
    """Change the color of the sender."""
    loggei.debug("%s()", indicate_tagged_results.__name__)

    loggei.info("User data: %s", user_data)

    # Make a toggle of the selected buttons
    if dpg.get_item_theme(item=sender) == orng_btn_theme:
        loggei.debug("Removing button theme")
        # Remove the button theme
        dpg.bind_item_theme(
            item=sender,
            theme=None,
        )
    else:
        # Turn the button orange
        tag = dpg.get_item_alias(item=sender)
        loggei.debug("Turning button orange")
        dpg.bind_item_theme(
            item=tag,
            theme=orng_btn_theme,
        )

    loggei.debug("%s() exiting", indicate_tagged_results.__name__)


def return_indicated_results() -> dict[str, dict[str, str]]:
    """Turn the results from individual to a collection."""
    loggei.debug("%s()", return_indicated_results.__name__)

    selected_items_dict: dict[str, dict[str]] = dict()

    # Read the contents of the database
    scan_results: list[dict] = wifi_load()

    [loggei.warning("Selected scan results: %s", i) for i in scan_results]

    # Get all of the alias themes
    for _, color in enumerate(scan_results, start=1):
        loggei.warning("Color: %s", color)
        # loggei.warning("Color[0]: %s", color[0])
        # loggei.warning("Color[1]: %s", color[1])
        loggei.warning("dpg color: %s", dpg.get_item_theme(color["mac"]))

        if dpg.get_item_theme(color["mac"]):
            selected_items_dict.update({color.get("ssid"): color})

    [loggei.warning("scan result Aliases selected: %s", i) for i in selected_items_dict]

    return selected_items_dict


def correlate_macs(chosen_mac: list[str], all_wifi_data: list[dict]) -> list[str]:
    """Compare the relevant octets of the MAC to all others."""
    loggei.debug("%s()", correlate_macs.__name__)

    all_macs: list[str] = [i.get("mac") for i in all_wifi_data]

    # Compare the first several octets of the chosen macs to all others
    correlated_macs: list[str] = list()

    for selected in chosen_mac:
        for mac in all_macs:
            if selected[:8] == mac[:8]:
                correlated_macs.append(mac)

    # Compare the last several octets of the chosen macs to all others
    for selected in chosen_mac:
        for mac in all_macs:
            if selected[-8:] == mac[-8:]:
                correlated_macs.append(mac)

    loggei.info("Raw Correlated MACs: %s", correlated_macs)

    # Compare the all except the last octet
    for selected in chosen_mac:
        for mac in all_macs:
            if selected[:-2] == mac[:-2]:
                correlated_macs.append(mac)

    # Remove the chosen mac if it is in the correlated macs
    for mac in correlated_macs:
        if mac in chosen_mac:
            correlated_macs.remove(mac)

    loggei.info("Correlated MACs: %s", correlated_macs)

    return correlated_macs


def ssid_from_mac(macs: list[str], all_data: list[dict]) -> list[str]:
    """Given a mac address, return the SSID."""

    loggei.debug("%s()", ssid_from_mac.__name__)

    ssid_list: list[str] = list()

    for mac in macs:
        for data in all_data:
            if mac == data.get("mac"):
                ssid_list.append(data.get("ssid"))

    [loggei.info(f"Matched SSIDs: {i}") for i in ssid_list]
    # Development and validation only
    # [
    # print(f"{F.GREEN if i.get('ssid') in ssid_list else F.WHITE}{i.get('ssid')}{R}")
    # for i in all_data
    # ]

    return ssid_list


def frequency_from_mac(macs: list[str], all_data: list[dict]) -> list[str]:
    """Given a mac address, return the frequency."""

    loggei.debug("%s()", frequency_from_mac.__name__)

    frequency_list: list[str] = list()

    for mac in macs:
        for data in all_data:
            if mac == data.get("mac"):
                frequency_list.append(data.get("frequency"))

    [loggei.info(f"Matched Frequencies: {i}") for i in frequency_list]
    # Development and validation only
    # [
    # print(f"{F.GREEN if i.get('frequency') in frequency_list else F.WHITE}{i.get('frequency')}{R}")
    # for i in all_data
    # ]

    return frequency_list


def activate_wifi_chase() -> None:
    """Send all the requisite information to the MGTron board."""
    loggei.debug("%s()", activate_wifi_chase.__name__)

    user_data: dict[str, str, int, int, float, str] = return_indicated_results()

    if not user_data:
        loggei.info("calling wifi_kill_all()")
        wifi_kill_all()
        return

    ssid: list[str] = [i.get("ssid") for i in user_data.values()]
    mac_address: list[str] = [i.get("mac") for i in user_data.values()]

    related_ssid = correlate_macs(mac_address, wifi_load())

    ssid.extend(ssid_from_mac(related_ssid, wifi_load()))

    # Filter out duplicates
    ssid = list(set(ssid))

    loggei.info("SSIDs' to search: %s", ssid)

    try:
        dpg.delete_item(item=129)
        dpg.delete_item(item="128")
    except SystemError as err:
        loggei.error("System error: %s", err)

    channel_list: list[int] = discern_avail_channels(dpg)

    loggei.info("Channel list: %s", channel_list)

    # If there are no channels available, then all available
    if not channel_list:
        channel_list: list[int] = [1, 2, 3, 4, 5, 6, 7, 8]

    # Iterations of which to rescan for chase
    count: int = 4  # len(user_data.keys())

    tracker = 0
    while tracker != count:
        if tracker >= 1:
            try:
                dpg.delete_item(item=129)
                dpg.delete_item(item="128")
            except SystemError as err:
                loggei.error("System error: %s", err)

                # Get the chase frequencies
                chase_freqs: list[float] = threaded_scan(
                    _dpg=dpg, linux_data=post_ssid, ssid=ssid
                )

        else:  # First iteration
            chase_freqs: list[float] = [i.get("frequency") for i in user_data.values()]

            # Include the other SSIDs from the AP
            chase_freqs.extend(frequency_from_mac(related_ssid, wifi_load()))

            loggei.info("Chase freqs: %s", set(chase_freqs))

        disable_scanning_mode(enable_btns=False)

        # Take advantage of the dedup characteristics of a set
        chase_freqs: set[float] = set(chase_freqs)

        # Chase three times
        chase(chase_freqs=chase_freqs, channel_list=channel_list)

        tracker += 1

    disable_scanning_mode(enable_btns=True)
    # Change the mssn_scan_jam button to blue
    dpg.bind_item_theme(
        item="mssn_scan_jam",
        theme=blue_btn_theme,
    )


def chase(chase_freqs: set[float], channel_list: list[int]) -> None:
    """Chase the WiFi signal."""
    loggei.info("%s()", chase.__name__)

    # Convert chase freqs to a dict[int, float]
    chase_freqs: dict[int, float] = {
        i: float(j) for i, j in enumerate(chase_freqs, start=1)
    }

    loggei.info("Chase freqs: %s", chase_freqs)

    send_to_n_cards(chase_freqs)

    dpg.configure_item(
        item="mssn_scan_jam",
        label="WIFI",
    )
    return None


def disable_scanning_mode(enable_btns: bool = True) -> None:
    """Disable the wifi scanning mode."""
    loggei.info("%s()", disable_scanning_mode.__name__)

    # Disable the open wifi window
    try:
        dpg.configure_item(item=129, show=False, modal=False)
        dpg.configure_item(item="128", show=False, modal=False)

        dpg.delete_item(item=129)
        dpg.delete_item(item="128")
    except SystemError:
        loggei.warning(msg="WiFi window already closed")

    # Make the wifi button blue
    dpg.bind_item_theme(
        item="mssn_scan_jam",
        theme=blue_btn_theme,
    )

    _ = enable_select_btns(*WIFI_BTNS_LIST, _dpg=dpg) if enable_btns else None


def wifi_kill_all() -> None:
    """Insert and auto send the top eight scanned channels."""
    loggei.debug("%s()", wifi_kill_all.__name__)

    loggei.info(msg="SCANNING...")

    # data: list[dict] = threaded_scan(
    # _dpg=dpg,
    # linux_data=find_signals_and_frequencies
    # )

    # Disable the open wifi window
    try:
        dpg.configure_item(item=129, show=False, modal=False)
        dpg.configure_item(item="128", show=False, modal=False)

        dpg.delete_item(item=129)
        dpg.delete_item(item="128")
    except SystemError:
        loggei.warning(msg="WiFi window already closed")

    saved_wifi_data: dict[int, float] = wifi_load()

    freq_and_strength: dict[int, float] = freqs_and_sigs(saved_wifi_data)

    threaded_wifi_scan(wifi_action=send_to_n_cards, vital_data=freq_and_strength)

    enable_select_btns(*WIFI_BTNS_LIST, _dpg=dpg)


def wifi_kill_window() -> None:
    """Close the wifi window upon pressing stop all."""
    loggei.debug("%s()", wifi_kill_window.__name__)
    loggei.debug("Deleting wifi window")

    loggei.info(msg="SCANNING...")

    # Disable the open wifi window
    try:
        dpg.configure_item(item=129, show=False, modal=False)
        dpg.configure_item(item="128", show=False, modal=False)

        dpg.delete_item(item=129)
        dpg.delete_item(item="128")
    except SystemError:
        loggei.warning(msg="WiFi window already closed")

    loggei.debug("Wifi window deleted, Enabling buttons")
    enable_select_btns(*WIFI_BTNS_LIST, _dpg=dpg)

    try:
        # Make the wifi button blue
        loggei.debug("Making wifi button blue")
        dpg.bind_item_theme(
            item="mssn_scan_jam",
            theme=blue_btn_theme,
        )
    except SystemError:
        loggei.warning(msg="WiFi window already closed")

    loggei.debug(msg="Scan jammer method finished")


def send_to_n_cards(freq_and_strength: dict[int, float]) -> None:
    """Send as many frequencies as there are card channels."""
    loggei.info("%s()", send_to_n_cards.__name__)

    loggei.info("pre 'send to cards' item length: %s", len(freq_and_strength))

    data_vehicle = Megatron()

    first_port_popped: str = ""

    loggei.info("Freq & Strength sorted: %s", freq_and_strength)

    port: dict[str, str] = return_teensy(device_names())

    # freq_and_strength: dict[int, float] = {
    #     1: 1310,
    #     2: 680,
    #     3: 741,
    #     4: 921,
    #     5: 1020,
    #     6: 1100,
    #     7: 1200,
    #     8: 1300,
    #     9: 1400,
    #     10: 1500,
    #     11: 1600,
    #     12: 1700,
    #     13: 1800,
    #     14: 1900,
    #     15: 2000,
    #     16: 2100,
    #     17: 2200,
    #     18: 2300,
    #     19: 2400,
    #     20: 2500,
    #     21: 2600,
    #     22: 2700,
    #     23: 2800,
    #     24: 2900,
    #     25: 3000,
    #     26: 3128,
    #     27: 3200,
    #     28: 3300,
    #     29: 3400,
    #     30: 3500,
    #     31: 3600,
    #     32: 3700,
    #     33: 3800,
    #     34: 3900,
    #     35: 4000,
    #     36: 4100,
    #     37: 4200,
    #     38: 4300,
    #     39: 4400,
    #     40: 4500,
    #     41: 4600,
    #     42: 4700,
    #     43: 4800,
    #     44: 4900,
    #     45: 5000,
    #     46: 5100,
    #     47: 5200,
    #     48: 5300,
    #     49: 5400,
    #     50: 5500,
    #     51: 5600,
    #     52: 5700,
    #     53: 5800,
    #     54: 5900,
    #     55: 6000,
    #     56: 6100,
    #     57: 6200,
    #     58: 6300,
    # }

    port: list[str] = list(port.values())

    # If there is 1 device, act accordingly
    if len(port) == 1:
        port: str = str(port[0])

        freq_and_strength: dict[int, float] = {
            k: v for k, v in freq_and_strength.items() if k <= 8
        }
    elif len(port) == 2:
        port = sorted(port)
        port[0], port[1] = port[1], port[0]
        first_port_popped = port[0]
    else:
        # Limit the number of scan results to the number of channels
        freq_and_strength: dict[int, float] = {
            k: v for k, v in freq_and_strength.items() if k <= len(port) * 8
        }

        [loggei.info("Ports available: %s", i) for i in sorted(port)]

        port = sorted(port)

        # Keep the first port first for unavoidable immediate popping
        port[0], port[1] = port[1], port[0]

        # Move card 0 to the end
        port[0], port[-1] = port[-1], port[0]

        # Capture card 0
        first_port_popped: str = port.pop()

        # Put card 0 in position to be the first to be assigned
        port.insert(2, first_port_popped)

        # Copy the card that will be last to be assigned so it can be assigned
        first_port_popped: str = port[0]

    start: int = 1

    loggei.warning(
        "Total available channels: %s",
        (len(port) if isinstance(port, list) else 1) * 8,
    )

    loggei.info("Final freqs: %s", len(freq_and_strength))

    _ = [
        (
            # Only way, at the time, to saturate all channels on all cards
            # This pops immediately, so its put back if the last port is needed
            port.pop(0)
            if (i % 8 if i % 8 else 8) == 1 and isinstance(port, list)
            else None,
            # no_power() if (i % 8 if i % 8 else 8) == 1 else None,
            loggei.info("\n") if (i % 8 if i % 8 else 8) == 1 else None,
            data_vehicle.change_freq(
                channel=i % 8 if i % 8 else 8,
                freq=freq,
                teensy_port=port[0] if isinstance(port, list) else port,
            ),
            data_vehicle.change_bandwidth(
                channel=i % 8 if i % 8 else 8,
                percentage=10,
                teensy_port=port[0] if isinstance(port, list) else port,
            ),
            data_vehicle.change_power(
                channel=i % 8 if i % 8 else 8,
                power_level=63 if freq > 0.0 else 0,
                teensy_port=port[0] if isinstance(port, list) else port,
            ),
            loggei.warning("Freq sent: %s", freq),
            loggei.warning("Channel sent to: %s", i % 8 if i % 8 else 8),
            loggei.warning("Port: %s", port[0] if isinstance(port, list) else port),
            # device_refresh() if i == 1 else None,
            # Since the list is immediately popped, put it back at the end
            port.append(first_port_popped) if first_port_popped not in port else None,
        )
        for i, freq in enumerate(freq_and_strength.values(), start=start)
    ]

    device_refresh()


def discern_avail_channels(_dpg: dpg) -> list[int]:
    """Determine which channel is available and return the channel number."""
    loggei.debug("%s()", discern_avail_channels.__name__)

    # Get all of the indicator colors
    indicator_color: list = [
        _dpg.get_item_theme(item=f"stats_{i}") for i in range(1, 9)
    ]

    loggei.info("Indicator color: %s", indicator_color)

    grey_theme = 30
    # Find out what channel numbers are available
    free_channels = indicator_color.count(grey_theme)

    loggei.info("Free channels: %s", free_channels)

    if not free_channels:
        loggei.warning(msg="No wifi channels available")
        return []

    # Transform all grey indicies to True and the rest to False
    indicator_color = [color == grey_theme for color in indicator_color]

    loggei.info("Indicator color: %s", indicator_color)

    # Keep track of the indices as the channel numbers to the new list
    channel_numbers = [i for i, color in enumerate(indicator_color, start=1) if color]

    loggei.info("Channel numbers returned: %s", channel_numbers)

    return channel_numbers


@DeprecationWarning
def wifi_factory(
    sender=None,
    app_data: Callable[
        [
            int,
        ],
        None,
    ] = None,
    user_data=None,
) -> None:
    """Take in the request and discern the appropriate wifi action."""
    loggei.debug("%s()", wifi_factory.__name__)

    loggei.info("calling wifi_chase()")
    activate_wifi_chase()


def threaded_wifi_scan(
    wifi_action: Callable[[dict[int, float]], None],
    vital_data: dict[int, float],
) -> None:
    """Scan for BLE signals and frequencies in a thread."""
    loggei.debug(msg=f"{threaded_wifi_scan.__name__}()")

    text_to_display = "INSTANTIATING RF TRANSMITTERS"

    with dpg.window(
        tag="wifi_send_all",
        no_scrollbar=True,
        no_collapse=True,
        no_resize=True,
        no_title_bar=True,
        modal=True,
        no_move=True,
        pos=(0, 0),
        width=880,
        height=720,
    ):
        dpg.add_text(tag="scan_text", default_value=text_to_display, pos=(300, 265))

    wifi = ThreadWithReturnValue(target=wifi_action, args=(vital_data,))
    wifi.start()

    sleep_delay: float = 0.5

    count = 0

    while wifi.is_alive():
        time.sleep(sleep_delay)
        count += 1
        dpg.configure_item(
            item="scan_text", default_value=text_to_display + "." * count
        )
        count = 0 if count > 3 else count
    count = 0

    count = 0 if count > 3 else count
    wifi = wifi.join()

    dpg.delete_item(item="wifi_send_all")

    # dpg.configure_item(
    # item="wifi_send_all",
    # modal=False,
    # )

    dpg.bind_item_theme(
        item="mssn_scan_jam",
        theme=blue_btn_theme,
    )

    return wifi


def main():
    """Run the main program."""
    loggei.info(msg="Main method called")

    send_to_n_cards({1: 2183.38})


if __name__ == "__main__":
    main()
