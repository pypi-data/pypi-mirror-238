# CHANGELOG

Author: Hunter, Christerpher
Author: Battieste, Nahjay

All notable changes will be appended here.

This file is especially formatted and shall not be edited outside of the format
shown below.
The version number shown in the GUI is pulled directly from this file.

This project, henceforth, will recongnize [semantic versioning](https://semver.org/).

## [⭐.✴️.✳️] - YEAR MONTH DAY

Here we write upgrade and change notes.

⭐ MAJOR version when you make incompatible API changes,

✴️ MINOR version when you add functionality in a backwards compatible manner

✳️ PATCH version when you make backwards compatible bug fixes.

-------------------------------------------------------------------------------

## ✳️ [2.27.1] - 2023 OCT 30

- feat: Take out the AP based on one SSID
- fix: remove all print statements and clean up code

## ✴️ [2.27.0] - 2023 OCT 26

- feat: Replaced WiFi algorithm with more reliable and more accurate results.
- feat: BLE results are stored in the database.

## ✴️ [2.26.0] - 2023 OCT 19

- feat: when an SSID is selected for jamming, All SSIDs from the same AP are also selected.

## ✳️ [2.25.3] - 2023 SEP 19

- docs: update changelog and copy
- feat: can successfully test for the item creation of all the the mission buttons
- fix: depracated 2 functions and removed pyautogui import
- feat: moving the mouse quicker


## ✳️ [2.25.2] - 2023 SEP 18

- fix: scroll speed

## ✳️ [2.25.1] - 2023 SEP 18

- chore: add scroll bar for reference during scrolling.
- fix: inverted the scrolling direction.
- fix: increased the scrolling speed.
- fix: aquire and lock the GIL in every frame.
- feat: improve scrolling feel.
- feat: click-down scrolling speed increase.
- chore: removed some fluff from slider implementation


## ✴️ [2.25.0] - 2023 SEP 8

- feat: added logging for handler registry call.
- fix: lock GIL as expected to be needed.
- fix: removed not used os import.
- chore: removed some fluff from slider implementation.
- wip: experimenting with pynput library.
- docs: update changelog.

## ✳️ [2.24.2] - 2023 SEP 5

- add: easy-install script
- fix: init script install permissions

## ✳️ [2.24.1] - 2023 SEP 1

- fix: wifi send all

## ✴️️ [2.24.0] - 2023 SEP 1

- chore: update dependency version
- feat: distance formula implemented
- add: 'dev-build-deploy' auto release gh action
- docs: update changelog and copy
- fix: cannot log json to log file

## ✳️ [2.23.3] - 2023 AUG 31

- fix: reciept of ble data; the ble_rs API changed.
- fix: cannot log json to log file.

## ✳️ [2.23.2] - 2023 AUG 31

- bump: forgot a manual step that make the correct version show.

## ✳️ [2.23.1] - 2023 AUG 31

- fix: gps calling
- chore: remove all prints

## ✴️️️ [2.23.0] - 2023 AUG 31

feat: Incorporate GPS positioning into BLE scans.


## ✳️ [2.22.7] - 2023 AUG 31

- fix: send proper types to api_rs endpoint.
- chore: clean out requirement; remove colorama from project.

## ✳️ [2.22.6] - 2023 AUG 30

- chore: move API launchers to globals/helpers; change port number for GPS.

## ✳️ [2.22.5] - 2023 AUG 30

- add: update dependency and remove BLE print statements.

## ✳️ [2.22.5] - 2023 AUG 30


## ✳️ [2.22.4] - 2023 AUG 25

- fix: deprecate shell version getter in place of .cpy version getter.

## ✳️ [2.22.4] - 2023 AUG 25

- feat: can change wifi button back to blue after default initail rf transmitters can.
- chore: added more logging to wifi_kill_window.
- fix: cleaned up more fluff and also using no_power in main.
- wip: am attempting to replicate the behavior of wifi kill all with a very similar function.
- doc: update changelog

## ✳️ [2.22.3] - 2023 AUG 18

- wip: correctly positioned buttons upon default wifi scan.
- feat: enabled scrollbar once again.
- fix: increased another bluetooth timeout.
- chore: added relevant logging statements to gui helpers.
- doc: update changelog.


## ✳️ [2.22.2] - 2023 AUG 14

- Added a feature to the GUI that allows BLE and WIFI to be toggled on and off, between each other.
- The BLE send all can be interrupted by the user with stop all, and functions as intended.
- Stop all now re enables all buttons upon the completion of the stop all function.

## ✳️ [2.22.1] - 2023 AUG 11

- Fixed a bug in which the stop all button would not stop the query of power commands.
- Fixed a bug in which the stop all button would not stop the wifi chase algorithm.
- Added a new database table to provide functionality for these changes.


## ✳️ [2.22.0] - 2023 AUG 7

- chore: turn prints into logs, remove deprecated db table.
- feat: fully selectable, sortable, and repeatable wifi scan results.
- refactor: wifi chase uses db.
- change: all relative imports to absolute imports


## ✳️ [2.21.2] - 2023 JULY 28

- WiFi send all occupies channels in numerical order.
- Failure of 'status' response responds with the command to soft reset the Teensy.


## ✴️️️ [2.21.1] - 2023 JULY 24

- Removed development block on Serial commands.
- Refactored Bluetooth table for better readability.
- Wifi Scan results are now sorted by signal strength.
- Wifi Scan results are scrollable.

## ✴️️️ [2.20.0] - 2023 JULY 13

- feat: wifi scan results can be toggled
- feat: allow repetitive scan of wifi signals.
- fix: autosend/chase w/ previous cancelled selected ssid
- chore: removed erroneous code

## ✳️ [2.19.4] - 2023 JULY 10

- Add scrollbar to the wifi scan results.
- Status indicator properly sends zero to power on the Teensy.

## ✳️ [2.19.1] - 2023 JULY 10

- Removed duplicates of wifi scan result frequencies.
- Fixed state awareness of the 'SEND ALL' button.
- Remove blockage to send commands to the Teensy.

## ✴️️️ [2.19.0] - 2023 JULY 07

- WiFi scan results are now selectable.
- WiFi scan results are in a pretty table.
- Send all button recognizes the state of WiFi and Bluetooth.
- Re-scan four times to check for hopping WiFi networks.
- Stop All button is globally live at all times.
- BLE send all algorithm is independent of the scan results.
- Re-wrote the delete button algorithm to be more robust.
- Refactored the table printing the wifi results

## ✳️ [2.18.5] - 2023 JUNE 30

- Fixed several bugs that kept the wifi result from populating.

## ✳️ [2.18.4] - 2023 JUNE 28

- Trials and tribulations of uploading to PyPI.

## ✴️️️ [2.18.0] - 2023 JUNE 26

- 'SEND ALL' button send requisite command depending on the state of wifi and bluetooth.
- Disable all action and mission buttons during a wifi or bluetooth scan.
- Implement an incremental print during wifi scan.

## ✳️ [2.17.3] - 2023 JUNE 21

- Fixed a bug in which the GUI would delete custom save when they were chosen.

## ✳️ [2.17.2] - 2023 JUNE 20

- Updated the README.md to reflect the new installation method.

## ✳️ [2.17.1] - 2023 JUNE 20

- Fixed a bug in which the GUI would hang if the BLE server was running.

## ✴️️️ [2.17.0] - 2023 JUNE 19

- Stabilized the BLE server starting and stopping.

## ✳️ [2.16.1] - 2023 JUNE 16

- Accounted for if the BLE sevice is not running.

## ✴️️ [2.16.0] - 2023 JUNE 14

- Changed file structure such that the pyproject.toml entry point is accurate.

## ✳️ [2.15.4] - 2023 JUNE 12
- Fixed a bug in which non-Teensy devices showed up on the GUI.

## ✳️ [2.15.3] - 2023 MAY 31
- Corrected Frequency Units header to reflect proper input range.

## ✳️ [2.15.2] - 2023 MAY 24

- Fixed a bug in which user could enter non-letter and non-character inputs
- Power/Bandwidth delineates to 100 or 0 if input is above maximum or below minimum

## ✳️ [2.15.1] - 2023 MAY 19

- Account for no Teensy detected.
- Make a name capital that was previously missed.

## ✴️️ [2.15.0] - 2023 MAY 18

- Add a toggle button to enable/disable auto sending the Mission button.

## ✳️ [2.14.1] - 2023 MAY 16

- Fixed a bug in which user could input power and bandwidth greater than 100 or less than 0.
- Autofill function now delineates all inputs to max of 100 or min of 0.

## ✴️ [2.14.0] - 2023 MAY 16

- Show eight disabled card select buttons on the right side and enable if device is present.

## ✴️ [2.13.0] - 2023 MAY 15

- Change button names to remove word "jam".
- Edited wifi button to show "SCANNING..." on press.

## ✳️ [2.12.1] - 2023 MAY 10

- Corrected an agregise mispelling of the wifi results functon
- Filled in missing values if the wifi scan returns less than 8 results.

## ✴️ [2.12.0] - 2023 MAY 09

- Change button names and functionality.


## ✳️ [2.11.1] - 2023 APR 24

- No longer reset input power to zero when 'kill all' is pressed.
- Send a trailing newline character to the MGTron when sending commands.
  - This is to ensure that the MGTron stops listening to receive commands.

## ✴️ [2.11.0] - 2023 APR 19

- When selecting a device, the state of the device will be displayed in the GUI.

## ✴️ [2.10.0] - 2023 APR 18

- Right click on the right-side 'card select' button to change the name of the card.

## ✳️ [2.9.1] - 2023 APR 18

- Remove the +/- buttons from all of the input fields.

## ✴️ [2.9.0] - 2023 APR 17

- Power input is now between 0 and 100.

## ✴️ [2.8.0] - 2023 APR 17

- Name a custom save as a mission button will load the custom save into the GUI.

## ✳️ [2.7.1] - 2023 APR 14

- Either choice of picking a device will change the colors accordingly.

## ✴️ [2.7.0] - 2023 APR 14

- The card select buttons on the right side of the GUI automattically turn green if the detected device is equivalent to the serial number provided in the config file.

## ✳️[2.6.1] - 2023 APR 13

- Captured all exceptions regarding starting the GUI with zero devices connected.

## ✴️ [2.6.0] - 2023 APR 13

- Right side buttons only appear if a device is connected.
- The refresh button now refreshes the currently selected device.

## ✴️ [2.5.0] - 2023 APR 12

- Can custom save and load configurations in real time

## ✳️[2.4.1] - 2023 APR 12

- Removed the text anomaly in the title bar

## ✴️ [2.4.0] - 2023 APR 11

- Swapped out JSON database for SQLite database

## ✴️[2.3.0] - 2023 FEB 20

- Change the button names to phonetic names
- Added a bluetooth scanning button
- Added bluetooth jamming functionality

## ✴️[2.2.0] - 2023 JAN 05

- Changed the phonetic mission buttons to be more explicit
- Removed the refresh and delete buttons

## ✴️[2.1.1] - 2022 DEC 28

- Make the status inidicators turn grey when a new device is selected

## ✴️[2.1.0] - 2022 DEC 14

- Added state awareness to the GUI
- The power and bandwith state are presented above the input fields

## ⭐[2.0.0] - 2022 DEC 13

- Can select and send commands to any number of MGTrons

## ✴️[1.3.0] - 2022 NOV 29

- Automated the Wifi scanning button.
- Implemented an automatic scan and jam button.

## ✴️[1.2.1] - 2022 NOV 10

- Wifi scan actually sorts by signal strength now.
- Added a getter function to grab the version from this file.

## ✴️[1.2.0] - 2022 NOV 10

- Reset all button only resets power.

## ✴️[1.1.0] - 2022 JUN 17

- Added a custom config file for every quick pick card option

## ⭐[1.0.0] - 2022 JUN 17

- Full save, delete, and select functionality of custom saved configurations

## ✴️[0.13.0] - 2022 JUN 16

- Live update of saved list after deletion
- Added delete and refresh button
- Added live update of load list

## ✴️[0.12.4] - 2022 JUN 16

- Card config file, if it doesnt exist, will auto populate with eigtht spot regardless of devices detected

## ✳️[0.12.3] - 2022 JUN 10

- Automatically overwrite or create save file if file is nonexistant or corrupted
- Mission buttons are configurable via config file location in `_config/`

## ✳️[0.12.2] - 2022 JUN 10

- Custom load functional!
- Reconfigured custom save

## ✳️[0.12.1] - 2022 JUN 7

- Removed the `find_dev.sh` script completely and retained that functionality
- Critical error in `find_dev.sh`; linux device finding listing script
- All phonetic mission buttons are configurable via config files
- Added YAML file to run PyPi update using GitHub Actions

## ✴️[0.12.0] - 2022 JUN 6

- The eight button on the right border correspond to up to eight cards
- Custom save configured and working

## ✴️[0.11.0] - 2022 JUN 3

- Scan and jam wifi automatically in RSSI order
- Added box around mission buttons

## ✳️[0.10.2] - 2022 JUN 3

- Automatically create config file and automatically populate config file
- Remove the word `CONFIG` from the buttons

## ✳️[0.10.1] - 2022 JUN 2

- Corrected multiple device bug
- Created an .ini config file and read contents
- Automatically fill in config if card_1 is not fillied in
- Changed name of all mission buttons
- Added `MISSIONS` above the mission buttons
- Card buttons turn blue if that number of cards are detected, disabled otherwise.

## ✴️[0.10.0] - 2022 JUN 1

- Added a set of buttons along the starboard side of the GUI
- New buttons highlight green when selected and grey when not
- When a device is chosen from the list the list promptly dissapears
- Added graceful exit

## ✳️[0.9.1] - 2022 MAY 31

- Device indicator reads no device detected if no device detected
- Fixed device listing bug
- Optimized scenario for if a single device detected

## ✴️[0.9.0] - 2022 MAY 25

- Now show device location and name
- Turn indicator buttons red if no device detected
- Add loggin to serial calls
- Connected devices are in numerical order

## ✳️[0.8.3] - 2022 MAY 25

- Added version number in bottom right of GUI

## ✳️[0.8.2] - 2022 MAY 24

- GUI will launch with no devices detected

## ✳️[0.8.1] - 2022 MAY 23

- Filling in list that holds all of the devices the GUI can access.

## ✴️[0.8.0] - 2022 MAY 23

- Changelog created.
- Project evolved enough to function and actuate hardware as expected.
