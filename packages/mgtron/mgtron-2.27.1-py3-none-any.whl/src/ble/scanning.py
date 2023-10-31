"""Make the API calls directly to the Rust API."""

import logging
import requests

loggei = logging.getLogger(name=__name__)


def ble_rs(target: str) -> dict:
    """Call the BLE RS API and return the data."""
    loggei.debug(msg=f"{ble_rs.__name__}()")

    port = 8080

    try:
        data = requests.get(
            url=f"http://localhost:{port}/{target}",
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
