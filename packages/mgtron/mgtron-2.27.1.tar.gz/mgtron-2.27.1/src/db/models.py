"""Database communicatation and execution of the SQL commands."""

from pathlib import Path
import pathlib
import logging
import sqlite3
from datetime import datetime


ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
WORKING = ROOT / "src"

# Define the input values
now = datetime.now()
date_accessed_value = datetime.now().strftime("%Y-%m-%d")

loggit = logging.getLogger(__name__)

# If the file does not exist create it
db_path: Path = Path(f"{WORKING}/db/mgtron_db.db")
init_path: Path = Path(f"{WORKING}/db/init_db.sql")


def read_sql_query(sql_path: pathlib.Path) -> str:
    """Read an SQL query from a file and returns it as a string."""
    return Path(sql_path).read_text()


# init the database
init_db = read_sql_query(init_path)


# Populate db if it does not exist
with sqlite3.connect(db_path) as connn:
    cursor = connn.cursor()
    cursor.executescript(init_db)
    connn.commit()
    # conn.close()


def save_channel_values_to_database(
    input_data: list[dict[str, str]], _path: str | Path = db_path
):
    """Save the input data to the database."""
    # Open a connection to the database and create a cursor
    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()
        cursors.executescript(init_db)
        conn.commit()

        # Insert into the save_name table and get the ID of the newly
        # inserted row
        try:
            cursors.execute(
                "INSERT INTO save_name (datetime, date_added,\
                    date_accessed, name) VALUES (?, ?, ?, ?)",
                (
                    input_data[0]["date"],
                    input_data[0]["date"],
                    input_data[0]["date"],
                    input_data[0]["save_name"],
                ),
            )
        except sqlite3.IntegrityError as err:
            # modal popup a dearpygui window
            loggit.error(err)
            # return

        save_name_id = input_data[0]["save_name"]

        # Insert into the channel tables using the save_name_id as a
        # foreign key
        cursors.execute(
            "INSERT INTO channel_1 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[0]["frequency"],
                input_data[0]["power"],
                input_data[0]["bandwidth"],
            ),
        )
        cursors.execute(
            "INSERT INTO channel_2 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[1]["frequency"],
                input_data[1]["power"],
                input_data[1]["bandwidth"],
            ),
        )
        cursors.execute(
            "INSERT INTO channel_3 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[2]["frequency"],
                input_data[2]["power"],
                input_data[2]["bandwidth"],
            ),
        )
        cursors.execute(
            "INSERT INTO channel_4 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[3]["frequency"],
                input_data[3]["power"],
                input_data[3]["bandwidth"],
            ),
        )
        cursors.execute(
            "INSERT INTO channel_5 (save_name_id, frequency,\
                power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[4]["frequency"],
                input_data[4]["power"],
                input_data[4]["bandwidth"],
            ),
        )
        cursors.execute(
            "INSERT INTO channel_6 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[5]["frequency"],
                input_data[5]["power"],
                input_data[5]["bandwidth"],
            ),
        )
        cursors.execute(
            "INSERT INTO channel_7 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[6]["frequency"],
                input_data[6]["power"],
                input_data[6]["bandwidth"],
            ),
        )
        cursors.execute(
            "INSERT INTO channel_8 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[7]["frequency"],
                input_data[7]["power"],
                input_data[7]["bandwidth"],
            ),
        )
        # Commit the changes to the database
        conn.commit()


def save_to_database_for_stop(input_string: str) -> None:
    """Save an input string to the database for the stop button functionality"""
    loggit.debug("Saving to the database function called")
    loggit.info(f"Saving {input_string} to the database")
    with sqlite3.connect(db_path) as conn:
        loggit.debug("Connected to the database and cursor object created")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stop_button_functionality (close_loop_keyword) VALUES (?)",
            [input_string],
        )
        conn.commit()
        return


def get_sql_stop_info() -> list[str]:
    """Get the stop button information from the database"""
    loggit.debug("Getting the stop button information from the database")
    with sqlite3.connect(db_path) as conn:
        loggit.debug("Connected to the database and cursor object created")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stop_button_functionality")
        result = cursor.fetchall()
        return result


def get_sql_details(
    save_name: str, _path: str | Path = db_path
) -> tuple[
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
]:
    """Load the data from the database and return it as a tuple."""
    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        cursors.execute(
            """
            SELECT
            channel_1.frequency,
            channel_1.power,
            channel_1.bandwidth,
            channel_2.frequency,
            channel_2.power,
            channel_2.bandwidth,
            channel_3.frequency,
            channel_3.power,
            channel_3.bandwidth,
            channel_4.frequency,
            channel_4.power,
            channel_4. bandwidth,
            channel_5.frequency,
            channel_5.power,
            channel_5.bandwidth,
            channel_6.frequency,
            channel_6.power,
            channel_6.bandwidth,
            channel_7.frequency,
            channel_7.power,
            channel_7.bandwidth,
            channel_8.frequency,
            channel_8.power,
            channel_8.bandwidth,
            channel_1.save_name_id,
            channel_2.save_name_id,
            channel_3.save_name_id,
            channel_4.save_name_id,
            channel_5.save_name_id,
            channel_6.save_name_id,
            channel_7.save_name_id,
            channel_8.save_name_id
            FROM save_name
            JOIN channel_1 ON channel_1.save_name_id = save_name.name
            JOIN channel_2 ON channel_2.save_name_id = save_name.name
            JOIN channel_3 ON channel_3.save_name_id = save_name.name
            JOIN channel_4 ON channel_4.save_name_id = save_name.name
            JOIN channel_5 ON channel_5.save_name_id = save_name.name
            JOIN channel_6 ON channel_6.save_name_id = save_name.name
            JOIN channel_7 ON channel_7.save_name_id = save_name.name
            JOIN channel_8 ON channel_8.save_name_id = save_name.name
            WHERE save_name.name = ?
            """,
            (save_name,),
        )

        result = cursors.fetchall()

    return result[0]  # type: ignore


def get_sql_save_names(_path: str | Path = db_path) -> list[str]:
    """Get the save names from the database"""
    loggit.debug("%s()", get_sql_save_names.__name__)

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()
        cursors.execute("SELECT name FROM save_name")
        result = cursors.fetchall()
        result = [i[0] for i in result]
        return result


def delete_sql_stop_info() -> None:
    """Delete the stop button information from the database."""
    loggit.debug("Deleting the stop button information from the database")
    with sqlite3.connect(db_path) as conn:
        loggit.debug("Connected to the database and cursor object created")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stop_button_functionality")
        conn.commit()
        return


def delete_sql_save_data(save_name: str, _path: str | Path = db_path):
    """Delete a save name from the database."""
    loggit.debug("%s()", delete_sql_save_data.__name__)

    loggit.info("Deleting save name %s from the database.", save_name)

    # print(f"Deleting save name {save_name} from the database.")

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        cursors.execute("DELETE FROM save_name WHERE name = ?", (save_name,))
        cursors.execute(
            "DELETE FROM\
            channel_1 WHERE save_name_id = ?",
            (save_name,),
        )
        cursors.execute(
            "DELETE FROM\
            channel_2 WHERE save_name_id = ?",
            (save_name,),
        )
        cursors.execute(
            "DELETE FROM\
            channel_3 WHERE save_name_id = ?",
            (save_name,),
        )
        cursors.execute(
            "DELETE FROM\
            channel_4 WHERE save_name_id = ?",
            (save_name,),
        )
        cursors.execute(
            "DELETE FROM\
            channel_5 WHERE save_name_id = ?",
            (save_name,),
        )
        cursors.execute(
            "DELETE FROM\
            channel_6 WHERE save_name_id = ?",
            (save_name,),
        )
        cursors.execute(
            "DELETE FROM\
            channel_7 WHERE save_name_id = ?",
            (save_name,),
        )
        cursors.execute(
            "DELETE FROM\
            channel_8 WHERE save_name_id = ?",
            (save_name,),
        )

        conn.commit()


def save_wifi_scan_results(
    ssid: str,
    mac: str,
    channel: int,
    frequency: float,
    signal: float,
    last_seen: int,
    save_name: str,
    sort_order: bool = False,
    _path: str | Path = db_path,
):
    """Save the wifi scan results to the database."""
    loggit.debug("%s()", save_wifi_scan_results.__name__)

    loggit.info("Saving wifi scan results to the database.")

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        insert_query = """
            INSERT INTO wifi_scan_results
            (ssid, mac, channel, frequency,\
        signal, last_seen, save_name_id, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """

        values = (
            ssid,
            mac,
            channel,
            frequency,
            signal,
            last_seen,
            save_name,
            sort_order,
        )

        cursors.execute(insert_query, values)

        conn.commit()


def save_ble_scan_results(
    mac: str,
    manufacturer: str,
    rssi: float,
    last_seen: int,
    save_name: str,
    distance: float,
    location: str,
    _path: str | Path = db_path,
):
    """Save the BLE scan results to the database."""
    loggit.debug("%s()", save_ble_scan_results.__name__)

    loggit.info("Saving BLE scan results to the database.")

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        insert_query = """
            INSERT INTO ble_scan_results
            (mac, manufacturer, rssi, last_seen, distance,\
        location, save_name_id)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """

        values = (mac, manufacturer, rssi, last_seen, distance, location, save_name)

        cursors.execute(insert_query, values)

        conn.commit()


def get_wifi_scan_results(
    _path: str | Path = db_path,
) -> tuple[str, str, str, str, int, int, int, str,]:
    """Load the data from the database and return it as a tuple."""
    loggit.debug("%s()", get_wifi_scan_results.__name__)

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        cursors.execute(
            """
            SELECT
            ssid,
            mac,
            channel,
            frequency,
            signal,
            last_seen
            FROM wifi_scan_results
            """
        )

        result = cursors.fetchall()

    return result


def get_ble_scan_results(
    _path: str | Path = db_path,
) -> tuple[str, str, str, str, int, int, int, str,]:
    """Load the data from the database and return it as a tuple."""
    loggit.debug("%s()", get_ble_scan_results.__name__)

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        cursors.execute(
            """
            SELECT
            mac,
            manufacturer,
            rssi,
            last_seen,
            distance,
            location
            FROM ble_scan_results
            """
        )

        result = cursors.fetchall()

    return result


def get_scan_result_sort_order(_path: str | Path = db_path) -> list[int]:
    """Get the sort order of the scan from the database."""
    loggit.debug("%s()", get_scan_result_sort_order.__name__)

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        cursors.execute(
            """
                SELECT sort_order
                FROM wifi_scan_results
                """
        )

        result = cursors.fetchone()

        return result


def set_scan_result_sort_order(sort_order: int, _path: str | Path = db_path):
    """Set the sort order of the scan in the database."""
    loggit.debug("%s()", set_scan_result_sort_order.__name__)

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        cursors.execute(
            """
            UPDATE wifi_scan_results
            SET sort_order = ?
            """,
            (sort_order,),
        )

        conn.commit()


def clear_wifi_table(_path: str | Path = db_path):
    """Clear the wifi table."""
    loggit.debug("%s()", clear_wifi_table.__name__)

    loggit.info("Clearing the wifi table.")

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        cursors.execute("DELETE FROM wifi_scan_results")

        conn.commit()


def clear_ble_table(_path: str | Path = db_path):
    """Clear the BLE table."""
    loggit.debug("%s()", clear_ble_table.__name__)

    loggit.info("Clearing the BLE table.")

    with sqlite3.connect(_path) as conn:
        cursors = conn.cursor()

        cursors.execute("DELETE FROM ble_scan_results")

        conn.commit()
