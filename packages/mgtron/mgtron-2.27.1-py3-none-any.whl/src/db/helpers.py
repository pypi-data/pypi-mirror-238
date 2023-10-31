"""Helper functions regarding the database for the GUI."""


import json
import logging
import sqlite3
from datetime import datetime
import pathlib
import dearpygui.dearpygui as dpg

from src.db.models import get_sql_save_names
from src.db.models import get_sql_details
from src.db.models import delete_sql_save_data
from src.db.models import save_channel_values_to_database
from src.db.models import save_wifi_scan_results
from src.db.models import get_wifi_scan_results
from src.db.models import set_scan_result_sort_order
from src.db.models import get_scan_result_sort_order
from src.db.models import save_ble_scan_results
from src.db.models import get_ble_scan_results


ROOT = pathlib.Path(__file__).resolve().parent.parent

# dd/mm/YY H:M:S
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
DB_PATH = pathlib.Path(ROOT / "db" / "mgtron_db.db")

loggey = logging.getLogger(name=__name__)


FREQ: dict[str, int] = {
    "chan_1": 0,
    "chan_2": 3,
    "chan_3": 6,
    "chan_4": 9,
    "chan_5": 12,
    "chan_6": 15,
    "chan_7": 18,
    "chan_8": 21,
}

POWS: dict[str, int] = {
    "chan_1": 1,
    "chan_2": 4,
    "chan_3": 7,
    "chan_4": 10,
    "chan_5": 13,
    "chan_6": 16,
    "chan_7": 19,
    "chan_8": 22,
}

BANDS: dict[str, int] = {
    "chan_1": 2,
    "chan_2": 5,
    "chan_3": 8,
    "chan_4": 11,
    "chan_5": 14,
    "chan_6": 17,
    "chan_7": 20,
    "chan_8": 23,
}

NAME: dict[str, int] = {
    "chan_1": 24,
    "chan_2": 25,
    "chan_3": 26,
    "chan_4": 27,
    "chan_5": 28,
    "chan_6": 29,
    "chan_7": 30,
    "chan_8": 31,
}


def live_refresh(alias: list[str]):
    """For as many aliases passed in, remove from the dpg registry."""
    loggey.debug(msg=f"{live_refresh.__name__}()")

    for i in dpg.get_aliases():
        for j in alias:
            if j in i:
                dpg.remove_alias(alias=i)
                loggey.debug("Removed alias: %s", i)


def get_save_data() -> list[dict[str, str]]:
    """Get the save data."""
    return [
        {
            "save_name": dpg.get_value(item="save_custom_input"),
            "power": dpg.get_value(f"power_{channel}"),
            "bandwidth": dpg.get_value(f"bandwidth_{channel}"),
            "frequency": dpg.get_value(f"freq_{channel}"),
            "date": dt_string,
        }
        for channel in range(1, 9)
    ]


def quick_save(sender, app_data, user_data) -> None:
    """Save the present inputs of the fields."""
    prelim_data: list[dict[str, dict[str, str]]] = [
        {
            f"channel {channel}": {
                "Power": dpg.get_value(f"power_{channel}"),
                "Bandwidth": dpg.get_value(f"bandwidth_{channel}"),
                "Frequency": dpg.get_value(f"freq_{channel}"),
                "Date": dt_string,
            },
        }
        for channel in range(1, 9)
    ]

    with open(file=f"{ROOT}/db/quick_save.json", mode="w") as file:
        file.write(json.dumps(obj=prelim_data, indent=2))
        loggey.info("Save Complete")


def quick_load(sender, app_data, user_data) -> None:
    """Load the last daved data."""
    saved_data: list = []

    try:
        loggey.info("Opening the quick save file: quick_save.json")
        with open(file=f"{ROOT}/db/quick_save.json") as file:
            saved_data = json.loads(file.read())
            [
                (
                    dpg.set_value(
                        item=f"power_{channel}",
                        value=saved_data[channel - 1][f"channel {channel}"]["Power"],
                    ),
                    dpg.set_value(
                        item=f"bandwidth_{channel}",
                        value=saved_data[channel - 1][f"channel {channel}"][
                            "Bandwidth"
                        ],
                    ),
                    dpg.set_value(
                        item=f"freq_{channel}",
                        value=saved_data[channel - 1][f"channel {channel}"][
                            "Frequency"
                        ],
                    ),
                )
                for channel in range(1, 9)
            ]
            loggey.info("Quick load complete")

    except SystemError:
        loggey.error("No saved data found")
        return


def custom_save() -> None:
    """Save config w/ a custom name."""
    loggey.debug("%s() executed", custom_save.__name__)

    try:
        save_data = get_save_data()

    except (
        TypeError,
        IndexError,
        KeyError,
        AttributeError,
        ValueError,
    ):
        loggey.warning(msg=f"database failure | {custom_save.__name__}()")

    # Clear input and close input
    dpg.set_value(item="save_custom_input", value="")
    dpg.configure_item(item="modal_save", show=False)

    save_channel_values_to_database(
        input_data=save_data,
    )


def custom_load(sender, app_data=None, user_data=None) -> None:
    """Load config /w a custom name."""
    loggey.info("%s() executed", custom_load.__name__)

    # print(f"\nsender: {sender}")

    loggey.debug(msg="Attempting to load custom save data")

    custom_load_to_sql: list[str] = []
    try:
        custom_load_to_sql = get_sql_save_names()
    except sqlite3.DatabaseError:
        loggey.warning(msg="No custom save file found")
    init_save_data_length = custom_load_to_sql.__len__()

    live_refresh(
        alias=[
            "load",
        ]
    )
    loggey.info(msg=f"Sender: {sender}")
    with dpg.window(
        modal=True,
        popup=True,
        tag="modal_loaded",
        pos=(
            0,  # dpg.get_viewport_client_width() // 2 - 100,
            0,  # dpg.get_viewport_client_height() // 2 - 100,
        ),
    ):
        _ = {
            (
                dpg.add_menu_item(
                    parent="modal_loaded",
                    label=unique,
                    tag=f"load_{itera + init_save_data_length}",
                    callback=load_chosen,
                    user_data=(unique, itera + init_save_data_length),
                ),
            )
            # if {sender, }.union({"custom_load_button", 220})  # set theory
            # else (
            #     dpg.add_menu_item(
            #         parent="modal_delete",
            #         label=unique,
            #         callback=delete_chosen,
            #         user_data=(unique, itera + init_save_data_length),
            #         tag=f"delete_{itera + init_save_data_length}",
            #         show=True,
            #     )
            # )
            for itera, unique in enumerate(custom_load_to_sql, start=0)
        }
        dpg.add_button(
            label="Close",
            parent="modal_loaded",
            tag="close_modal_loaded",
            callback=lambda: dpg.configure_item(item="modal_loaded", show=False),
        )


def load_chosen(
    sender=None, app_data=None, user_data: tuple[str, int] = ("", 0)
) -> None:
    """Take in the chosen file to be loaded to the input fields of the gui."""
    loggey.info(f"{load_chosen.__name__}() executed")

    _custom_load = get_sql_details(save_name=user_data[0])
    _ret_data: tuple = _custom_load

    _ = [
        (
            dpg.set_value(item=f"freq_{itera}", value=_ret_data[FREQ[f"chan_{itera}"]]),
            dpg.set_value(
                item=f"power_{itera}", value=_ret_data[POWS[f"chan_{itera}"]]
            ),
            dpg.set_value(
                item=f"bandwidth_{itera}", value=_ret_data[BANDS[f"chan_{itera}"]]
            ),
        )
        for itera in range(1, 9)
    ]


def delete_chosen(
    sender=None,
    app_data=None,
    user_data: tuple[str, int] = (str(), int()),
) -> None:
    """Delete a saved file."""
    # Get the list of saved objects
    _custom_load = get_sql_save_names()
    init_save_data_length = _custom_load.__len__()
    live_refresh(
        alias=[
            "delete",
        ]
    )

    with dpg.window(
        modal=True,
        popup=True,
        tag="modal_delete",
        pos=(
            0,  # dpg.get_viewport_client_width() // 2 - 100,
            0,  # dpg.get_viewport_client_height() // 2 - 100,
        ),
    ):
        _ = [
            dpg.add_menu_item(
                parent="modal_delete",
                label=unique,
                callback=delete_it,
                user_data=(unique, itera + init_save_data_length),
                tag=f"delete_{itera + init_save_data_length}",
                show=True,
            )
            for itera, unique in enumerate(_custom_load, start=0)
        ]
        dpg.add_button(
            label="Close",
            parent="modal_delete",
            tag="close_modal_delete",
            callback=lambda: dpg.configure_item(item="modal_delete", show=False),
        )

    loggey.info(
        "Live update of delete and load menu items complete\
            | %s()",
        delete_chosen.__name__,
    )


def delete_it(
    sender=None,
    app_data=None,
    user_data: tuple[str, int] = (str(), int()),
) -> None:
    """Delete the chosen database item."""
    loggey.debug(msg=f"{delete_it.__name__}() executed")

    # print(f"Sender: {sender}")
    # print(f"App data: {app_data}")
    # print(f"User data: {user_data[0]}")

    # Delete the selected item from the database
    delete_sql_save_data(save_name=user_data[0])


def check_and_load_config(button_name: str) -> dict[str, list]:
    """Check database for config button as the name of the saved config."""
    loggey.debug(msg=f"{check_and_load_config.__name__}()")
    config_data: dict[str, list] = {}

    # Check the sql database for the name of the button
    save_names = get_sql_save_names()

    # Remove new lines and rejoin sentence; this is ! robust
    button_name = button_name.replace("  ", " ").replace("\n", "")

    loggey.info("Button name %s: ", button_name)

    if button_name in save_names:
        loggey.debug("Button name %s  found in DB", button_name)

        # Get the config from the database
        config = get_sql_details(save_name=button_name)

        loggey.debug(config)

        # Get the channel, frequency, power, and bandwidth
        channel: list[int] = [int(i) for i in range(1, 9)]
        frequency: list[float] = [
            float(config[FREQ[f"chan_{i}"]]) for i, _ in enumerate(FREQ, start=1)
        ]
        power: list[int] = [
            int(config[POWS[f"chan_{i}"]]) for i, _ in enumerate(POWS, start=1)
        ]
        bandwidth: list[int] = [
            int(config[BANDS[f"chan_{i}"]]) for i, _ in enumerate(BANDS, start=1)
        ]

        # Store the config in a dictionary
        config_data: dict[str, list] = {
            "channel": channel,
            "freq": frequency,
            "power": power,
            "bw": bandwidth,
        }

    return config_data


def wifi_save(
    scan_data: list[list],
    db_path: str | pathlib.Path = DB_PATH,
) -> None:
    """Save the wifi config to the database."""
    loggey.debug("%s()", wifi_save.__name__)
    loggey.debug("DB path: %s", db_path)

    for data in scan_data:
        _ = save_wifi_scan_results(
            ssid=data[0].strip(),
            mac=data[1],
            channel=data[2],
            signal=data[4],
            frequency=data[3],
            last_seen=data[-1],
            save_name=data[1],
        )


def ble_save(
    scan_data: list[list],
    db_path: str | pathlib.Path = DB_PATH,
) -> None:
    """Save the wifi config to the database."""
    loggey.debug("%s()", ble_save.__name__)
    loggey.debug("DB path: %s", db_path)

    for data in scan_data:
        _ = save_ble_scan_results(
            mac=data[0],
            manufacturer=data[1],
            rssi=data[2],
            last_seen=0.00,
            distance=data[3],
            location=data[4],
            save_name=data[0],
        )


def wifi_load() -> list[dict]:
    """Return the WiFi data stored in the database."""
    loggey.debug("%s()", wifi_load.__name__)

    # Get the wifi scan results
    wifi_data = get_wifi_scan_results()

    # process the return data
    wifi_data = [
        {
            "ssid": data[0],
            "mac": data[1],
            "channel": data[2],
            "frequency": data[3],
            "signal": data[4],
            "last_seen": data[5],
        }
        for data in wifi_data
    ]

    _ = [
        loggey.warning("received Scan data: %s", j)
        for i in wifi_data
        for j in i.items()
    ]

    return wifi_data


def ble_load() -> list[dict]:
    """Return the BLE data stored in the database."""
    loggey.debug("%s()", ble_load.__name__)

    # Get the wifi scan results
    ble_data = get_ble_scan_results()

    # process the return data
    ble_data = [
        {
            "mac": data[0],
            "manufacturer": data[1],
            "rssi": data[2],
            "distance": data[3],
            "location": data[4],
            "last_seen": data[5],
        }
        for data in ble_data
    ]

    _ = [
        loggey.warning("received Scan data: %s", j) for i in ble_data for j in i.items()
    ]

    return ble_data


def get_sort_order() -> bool:
    """Get the sort order from the database."""
    loggey.debug("%s()", get_sort_order.__name__)

    # Get the sort order from the database
    sort_order = get_scan_result_sort_order()

    loggey.info("Sort order: %s", sort_order[0])

    return sort_order[0]


def set_sort_order(sort_order: bool) -> None:
    """Set the sort order in the database."""
    loggey.debug("%s()", set_sort_order.__name__)

    # Set the sort order in the database
    set_scan_result_sort_order(sort_order=sort_order)


def main():
    """Execute the main program."""
    import time

    wifi_scan_data: list[dict] = []

    # Create artificial wifi data
    wifi_scan_data = [
        {
            "ssid": "SSID_1",
            "mac": "00:00:00:00:00:00",
            "channel": 1,
            "signal": -50,
            "frequency": 2.412,
            "last_seen": "WPA2",
        },
        {
            "ssid": "SSID_2",
            "mac": "00:00:00:00:00:01",
            "channel": 2,
            "signal": -60,
            "frequency": 2.417,
            "last_seen": "WPA2",
        },
        {
            "ssid": "SSID_3",
            "mac": "00:00:00:00:00:02",
            "channel": 3,
            "signal": -70,
            "frequency": 2.422,
            "last_seen": "WPA2",
        },
        {
            "ssid": "SSID_4",
            "mac": "00:00:00:00:00:03",
            "channel": 4,
            "signal": -80,
            "frequency": 2.427,
            "last_seen": "WPA2",
        },
    ]

    # Save the data to the database
    wifi_save(scan_data=wifi_scan_data)

    time.sleep(1)
    # Load the data from the database
    wifi_scan_data_4 = wifi_load()

    # Print the data
    print(f"Wifi scan data 4: {wifi_scan_data_4}")


if __name__ == "__main__":
    main()
