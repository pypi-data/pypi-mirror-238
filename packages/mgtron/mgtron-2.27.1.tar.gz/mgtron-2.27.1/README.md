# MGTron Signal Generator Interface

## A functional mutlti card interface for the MGTron Signal Generator

This project revolves around the MGTron signal generator.  The graphical user interface (GUI) is written purely in python.  There are some facets that utilize linux command line tools.  Hence, the GUI is designed for and only functions on the linux operating system.  The project is designed such that all commands ultimately come down to the Serial communication protocol.  Serial communication, via the  [pyserial](https://pyserial.readtodata.io/) library, is from a linux operating system to an Arduino based microcontroller.  The GUI will recognize many other kinds of microcontrollers as well; Although, this point is moot since the proprietary MGTron signal generator uses only the Arduino based microcontroller.

* Set the frequency, power, and bandwidth of each of the eight channels.
* Send to all channels at once or individually.
* Easy one-click to turn off a generating channel.
* Choose a specific device based on its serial number.
* Easy install to most Linux distributions.
* Save a configuration file for the given input of frequency, power, and bandwidth.
* Pre-configurable configurations for up to eight devices.
* Pre-configurable mission buttons.
* Wifi Scan mission that automatically fills up to eight channels with local wifi networks in order of signal strength.
* Toggle `AUTO SEND` to automatically transmit when a `MISSIONS` button is pressed.
* Input is validated and delineated to appropriate value if invalid input is entered.

## Reserved Frequencies: G27 Band
The frequency ranges identified below are reserved for military use and are not allowed to be used by the MGTron Signal Generator. If a frequency in these ranges is entered, the MGTron will not send it.
* 224.99 - 328.59 MHz
* 335.39 - 399.91 MHz
* 1349.99 - 1390.01 MHz

## Special Features

* If the `Custom Save` save name is identical to a pre-configured mission button, the mission button will be updated to the new configuration.
* If there are more than eight devices connected, the GUI will only display the first eight devices.  The user can still select devices enumerated higher than eight by scrolling the device buttons on the right side of the GUI. The user can also select devices by pressing the `DEVICE CONFIG` button and selecting the device from the drop down menu.

## Visualization

![mgtron_demo](https://user-images.githubusercontent.com/25860608/174464184-1511b551-a6ca-4b74-84f8-aeec5d31d9a4.gif)

## Installation

### Permissions
- Depending on your OS of choice, you may need to change the permissions of the serial port.  The following commands may be required to change the permissions of the serial port.
* `sudo chmod 777 /dev/ttyACM*` - temporary and **UNSAFE** fix
* `sudo usermod -a -G dialout $USER` - permanent fix on Debian based distributions; **reboot required**
* `sudo usermod -a -G uucp $USER` - permanent fix; **reboot required**


### Requirements

* Python 3.10+
* git

### install from PyPI

- Go to a directory where you want to install the package.

`touch .env`

- Place the `sudo` password in the `.env` file. - **This is required for the WiFi scanning.**

`python -m venv venv` - Optional, but recommended.

`source venv/bin/activate` - Required, if last line is executed.

`pip install mgtron`

`mgtron`

## Known Issues


* Version
  * `Update to Python3.10`

### GUI never launches
* The Teensy is not properly initialized. This appears to happen randomly in testing.  The solution is to power cycle the Teensy.  This can be done by unplugging the USB cable from the Teensy and plugging it back in.  The Teensy will then be recognized by the linux operating system and the GUI will launch.
* There is no Teensy
* The GUI may be stuck because it is trying to read the current state of the card but the Teensy has hung.
* The log file is named mg.log and is located in the mg_tron directory.  The log file is overwritten everytime the GUI launches.
* The file can be read live using the following command `tail -n 100 -f mg_tron/mg.log`
* It is important to remember to input the full path of the log file.

### Wifi Scan broken
* Ensure wifi is enabled on the device.
