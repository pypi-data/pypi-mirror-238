"""Make the API calls directly to the GPS API."""

import logging
import requests

loggei = logging.getLogger(name=__name__)


def gps_py(target: str) -> dict:
    """Call the BLE RS API and return the data."""
    loggei.debug(msg=f"{gps_py.__name__}()")

    port = 8085

    try:
        data = requests.get(
            url=f"http://localhost:{port}/all_serial_data/{target}",
            headers={"Content-Type": "application/json"},
            timeout=23,
        )

        if data.status_code != 200:
            loggei.error(msg=f"BLE API returned {data.status_code}")
            return {}

        loggei.info(msg=f"BLE API raw response: {data}")

        data: dict = data.json()

        return data

    except requests.exceptions.ConnectionError as err:
        loggei.error(msg=f"BLE API not running: {err}")
        return {"Status": requests.status_codes}


def process_gps(target: str) -> dict:
    """Process the GPS data."""
    loggei.debug("%s()", process_gps.__name__)

    return_dict: dict[str, str] = {}

    match target:
        case "lat_long":
            raw_gps: dict[str, str] = gps_py(target)
            try:
                lat: str = raw_gps[0].strip('{').strip('}').split(',')[0]
                long: str = raw_gps[0].strip('{').strip('}').split(',')[1]
                loggei.info(msg=f"lat: {lat}, long: {long}")
            except KeyError:
                lat = "latitude: N/A"
                long = "longitude: N/A"

            return_dict.update({
                "latitude": lat.split(':')[1],
                "longitude": long.split(':')[1]
            })

            return return_dict

        case "altitude":
            raw_gps: dict[str, str] = gps_py(target)
            altitude: str = raw_gps[0].strip('{').strip('}').split(',')[0]

            return_dict.update({
                "altitude": altitude.split(':')[1].strip('"')
            })

            print(return_dict)

            return return_dict

        case "utc_time":
            raw_gps: dict[str, str] = gps_py(target)
            utc_time: str = raw_gps[0].strip('{').strip('}').split(',')[0]

            return_dict.update({
                "utc_time": utc_time.split('":')[1].strip('"')
            })

            print(return_dict)

            return return_dict


def main():
    """Test reception of data."""
    process_gps("altitude")


if __name__ == "__main__":
    main()
