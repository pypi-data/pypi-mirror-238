"""Process the BLE data."""

import time
import logging

import dearpygui.dearpygui as dpg

from src.ble.scanning import ble_rs

from src.globals.helpers import ThreadWithReturnValue
from src.gps.scanning import process_gps

from src.db.helpers import ble_save


loggei = logging.getLogger(name=__name__)


def ble_data(company: bool) -> dict[str, str | int]:
    """Collate the da from the BLE API and return it."""
    loggei.debug(msg=f"{ble_data.__name__}()")

    target: tuple[str, str] = "dev", "rssi"

    # Grab the data from the API
    data = ble_rs(target=target[0]) if not company else ble_rs(target=target[1])

    loggei.info(msg=data)

    # If the data is empty, return an empty dict
    if not data:
        return {}

    # Grab the data from the dict
    if not company:
        # macs, rssi = (data.keys(), data.values())
        # print(f"RSSI {list(rssi)}")
        return data

    else:
        # macs, companies = (data.keys(), data.values())
        # print(f"Companies {list(companies)}")
        return data

    # return [
    #     list(macs),
    #     list(rssi)
    # ] if not company else [
    #     list(macs),
    #     list(companies)
    # ]


def threaded_ble_scan(company: bool) -> tuple[list, list]:
    """Scan for BLE signals and frequencies in a thread."""
    loggei.debug(msg=f"{threaded_ble_scan.__name__}()")

    dpg.configure_item(
        item="12",
        modal=True,
    )
    dpg.configure_item(
        item="ble_list",
        width=880,
        height=680,
    )

    dpg.add_text(tag="scan_text", default_value="SCANNING RSSI", pos=(400, 265))

    ble_man = ThreadWithReturnValue(target=ble_data, args=(company[0],))

    ble_man.start()

    ble_rssi = ThreadWithReturnValue(target=ble_data, args=(company[1],))
    sleep_delay: float = 0.5

    count = 0

    while ble_man.is_alive():
        time.sleep(sleep_delay)
        count += 1
        dpg.configure_item(
            item="scan_text", default_value="SCANNING RSSI" + "." * count
        )
        count = 0 if count > 3 else count
    count = 0

    ble_rssi.start()

    while ble_rssi.is_alive():
        time.sleep(sleep_delay)
        count += 1
        dpg.configure_item(
            item="scan_text", default_value="SCANNING MANUFACTURER" + "." * count
        )
        count = 0 if count > 3 else count
    ble_man: dict[str, str] = ble_man.join()
    ble_rssi: dict[str, int] = ble_rssi.join()

    ble_data_complete: dict[str, list[str, str, int]] = match_macs(
        base=ble_man, matcher=ble_rssi
    )

    dpg.delete_item(item="scan_text")

    dpg.configure_item(
        item="12",
        modal=False,
    )

    ble_info = []
    # Save the results to the database
    for mac in ble_data_complete:

        # print(f"mac: {ble_data_complete[mac][3]}")
        ble_info.append(
            [
                mac,  # MAC Address
                ble_data_complete[mac][0],  # MANUFACTURER
                ble_data_complete[mac][1],  # RSSI
                ble_data_complete[mac][3],  # DISTANCE
                ble_data_complete[mac][4],  # LOCATION
            ]
        )

    # print(f"ble_info: {ble_info}")
    ble_save(scan_data=ble_info)

    return ble_data_complete


def match_macs(
    base: dict[str, str], matcher: dict[str, int]
) -> dict[str, list[str, str, int]]:
    """Take two different types of BLE scans and match them."""
    loggei.debug(msg=f"{match_macs.__name__}()")

    loggei.info(f"base: {len(base)}")
    loggei.info(f"matcher: {len(matcher)}")

    ble_return: dict[str, str] = {}

    macs: dict[str, str] = {}

    for match in matcher:
        macs.update({match["mac_address"]: match["hex"] for _ in match})

    loggei.info(f"macs: {macs}")

    # Create a set of the MAC addresses from base and matcher
    base_set = set(base.keys())
    matcher_set = set(macs.keys())

    loggei.info(f"base_set: {base_set}")
    loggei.info(f"matcher_set: {matcher_set}")

    base_set = {mac.split("]")[1] for mac in base_set}

    base_split = {mac.split("]")[1]: base[mac] for mac in base}

    loggei.info(f"base_set split: {base_set}")

    # Find the intersection of the two sets
    ble_intersection = base_set.intersection(matcher_set)

    loggei.info(f"ble_intersection: {ble_intersection}")

    gps_data: dict[str, str] = process_gps("lat_long")
    gps_data: str = gps_data.get("latitude") + gps_data.get("longitude")

    loggei.info(f"gps_data: {gps_data}")

    # print(f"base_split: {base_split}", end="\n\n")

    company: dict[str, str] = {}
    rssi: dict[str, int] = {}
    air_tag: dict[str, str] = {}
    # distance: dict[str, float] = {}

    try:
        # Seperately store the company, rssi and air_tag
        for scan_result in matcher:
            company.update({scan_result["mac_address"]: scan_result["company"]})
            air_tag.update({scan_result["mac_address"]: scan_result["air_tag"]})
            # distance.update(
            # {scan_result["mac_address"]: scan_result["distance"]})

            rssi.update(
                {scan_result["mac_address"]: base_split.get(scan_result["mac_address"])}
            )
    except KeyError as err:
        # print(f"KeyError: {err} not in base")
        loggei.error(f"KeyError: {err} not in base")
        # msg=f"KeyError: {scan_result['mac_address']} not in base")

        rssi.update({scan_result["mac_address"]: -99})
        company.update({scan_result["mac_address"]: "Unknown"})
        air_tag.update({scan_result["mac_address"]: "Unknown"})
        # distance.update({scan_result["mac_address"]: 0})

    loggei.info(f"company: {company}")
    loggei.info(f"rssi: {rssi}")
    loggei.info(f"air_tag: {air_tag}")

    # Collate the values from the intersection of two seperate scans
    for mac in ble_intersection:
        ble_return.update({mac: [company[mac]]})
        for key, value in base.items():
            if mac in key:
                ble_return[mac].append(value)
                ble_return[mac].append(air_tag[mac])
                ble_return[mac].append(rssi_to_distance(rssi[mac]))
                ble_return[mac].append(gps_data)

    loggei.info(f"{match_macs.__name__} ble_return: {ble_return}")

    return ble_return if ble_return else {"BLE Scan Failed": ["scan failed"]}


def rssi_to_distance(rssi: int) -> float:
    """Convert RSSI to distance."""
    loggei.debug(msg=f"{rssi_to_distance.__name__}()")

    # https://github.com/smart-sensor-devices-ab/python_bluetooth_device_distance_meter/blob/master/distance.py

    # print(f"init rssi: {rssi}")

    n = 2
    mp = -69
    return round(10 ** ((mp - (int(rssi))) / (10 * n)), 2)
