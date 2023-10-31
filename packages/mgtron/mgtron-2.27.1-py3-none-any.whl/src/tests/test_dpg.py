import pytest
import dearpygui.dearpygui as dpg
import pathlib
from typing import Any

from src.gui.helpers import card_selection
from src.gui.helpers import return_teensy, device_names
from src.gui.helpers import device_finder
from src.wifi.helpers import activate_wifi_chase
from src.ble.helpers import bluetooth_defeat
from src.gui.helpers import populate_right_side_buttons
from src.gui.helpers import change_card_name
from src.gui.helpers import compare_device_serial_to_config
from src.gui.helpers import tooltips


""" use of the pathlib module to get the root directory of the project """
ROOT = pathlib.Path(__file__).resolve().parent.parent

################
# DPG FIXTURES #
################

""" GENERAL FIXTURES """


# Fixture to create a dpg context
@pytest.fixture(scope="function")
def dpg_context():
    dpg.create_context()
    yield
    dpg.destroy_context()


# Fixture to recreate the GUI context
@pytest.fixture(scope="function")
def dpg_complex_context(dpg_context):
    """Fixture to recreate the GUI context"""

    # Creating Global Variables Used in the GUI
    RESOLUTION: list[int] = [1250, 735]  # 1200x800 initially
    POWER: bool = bool()
    ROW_HEIGHT: int = 78
    ADJUSTMENT: int = -25
    DIVISOR: float = 1.5
    SEND_RESET_ALL_HEIGHT: int = 695
    CUSTOM_CONFIG_HEIGHT: int = 300
    QUICK_CONFIG_HEIGHT: int = 480
    DEMO_HEIGHT: int = -470
    WIFI_HEIGHT: int = -400
    CELLUAR_HEIGHT: int = -560
    MAIN_TABLE_HEIGHT: int = 1
    BUTTON_WIDTH = 120

    # Dummy version
    __version__ = "2.25.3"

    # Green Button Theme
    with dpg.theme() as grn_btn_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0, 255))  # GREEN

    # Red Button Theme
    with dpg.theme() as red_btn_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # RED

    # Blue Button Theme
    with dpg.theme() as blue_btn_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))  # BLUE

    # Grey Button Theme
    with dpg.theme() as grey_btn_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (105, 105, 105, 255))  # GREY

    # Grey Column Theme
    with dpg.theme() as grey_column_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (185, 185, 185, 255))  # WHITE

    with dpg.font_registry():
        default_font_added: int | str = str()
        ital_font: int | str = str()
        bold_font: int | str = str()
        small_font: int | str = str()

        try:  # Stop gap incase the files cannot be found
            default_font_added = dpg.add_font(
                file=f"{ROOT}/gui/fonts/MesloLGS NF Regular.ttf", size=40
            )
            ital_font = dpg.add_font(
                file=f"{ROOT}/gui/fonts/MesloLGS NF Italic.ttf", size=20
            )
            bold_font = dpg.add_font(
                file=f"{ROOT}/gui/fonts/MesloLGS NF Bold Italic.ttf", size=40
            )
            small_font = dpg.add_font(
                file=f"{ROOT}/gui/fonts/MesloLGS NF Italic.ttf", size=13
            )
        except SystemError:
            pass

    with dpg.window(
        label="MGTron Control",
        tag="Primary Window",
        height=RESOLUTION[0],
        width=RESOLUTION[1],
        pos=(0, 0),
        no_scrollbar=True,
        horizontal_scrollbar=False,
    ):
        # Header Column Channel
        with dpg.child_window(
            pos=(0,),  # (x, y)
            width=40,
            height=ROW_HEIGHT - ADJUSTMENT,
            border=False,
        ):
            dpg.add_text(default_value="CH", pos=(19, 39 - ADJUSTMENT + 5))

        # Header Column Frequency
        with dpg.child_window(
            pos=(50,),  # (x, y)
            width=250,
            height=ROW_HEIGHT - ADJUSTMENT,
            border=False,
        ):
            dpg.add_text(
                default_value="FREQ: 50 MHz to 6400 MHz",
                pos=(10, 39 - ADJUSTMENT + 5),
            )

            # Header Column Power
        with dpg.child_window(
            pos=(300,),  # (x, y)
            width=150,
            tag="col_pwr",
            height=ROW_HEIGHT - ADJUSTMENT,
            border=False,
        ):
            dpg.add_text(
                default_value="PWR: 0 - 100%",
                pos=(
                    dpg.get_item_width(item="col_pwr") / 7,
                    39 - ADJUSTMENT + 5,
                ),
            )

        # Header Column Bandwidth
        with dpg.child_window(
            pos=(500,),  # (x, y)
            tag="col_bw",
            width=155,
            height=ROW_HEIGHT - ADJUSTMENT,
            border=False,
        ):
            dpg.add_text(
                default_value="BW: 0 - 100%",
                pos=(
                    dpg.get_item_width(item="col_bw") / 7,
                    39 - ADJUSTMENT + 5,
                ),
            )

        #######################
        # SEND and INDICATORS #
        #######################
        for i in range(8):
            # First Column
            with dpg.child_window(
                tag=f"row_{i+1}",
                pos=(
                    0,
                    ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT,
                ),  # (x, y)
                width=50,
                height=ROW_HEIGHT,
            ):
                dpg.add_text(
                    default_value=str(i + 1),
                    tag=f"channel_{i+1}",
                    pos=(13, ROW_HEIGHT // 2 - 21),
                )

            # Frequency Column Input
            with dpg.child_window(
                label=f"CHANNEL {i+1}",
                tag=f"freq_win_{i+1}",
                pos=(
                    50,
                    ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT,
                ),  # (x, y)
                width=250,
                height=ROW_HEIGHT,
            ):
                dpg.add_input_text(
                    tag=f"freq_{i+1}",
                    decimal=True,
                    # default_value=650.00 * ((i + 1)),
                    # min_value=50.00, max_value=6400.00,
                    # min_clamped=True, max_clamped=True,
                    width=dpg.get_item_width(item=f"freq_win_{i+1}") // 1.8,
                    # step=1, step_fast=100,
                    pos=(
                        dpg.get_item_pos(item="freq_win_1")[0],  # x
                        ROW_HEIGHT // 2 - 15,  # y
                    ),
                )

                # Indicate the frequency as queried from the
                # device
                dpg.add_text(
                    default_value="",
                    tag=f"frequency_{i+1}_indicator",
                    pos=(dpg.get_item_width(item=f"freq_{i+1}") / 1.36, 0),
                )

            # Power Column Input
            with dpg.child_window(
                label=f"CHANNEL {i+1}",
                tag=f"power_win_{i+1}",
                pos=(
                    300,
                    ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT,
                ),  # (x, y)
                width=180,
                height=ROW_HEIGHT,
            ):
                dpg.add_input_text(
                    tag=f"power_{i+1}",
                    decimal=True,
                    # min_value=0, max_value=100,
                    # min_clamped=True, max_clamped=True,
                    width=dpg.get_item_width(item=f"power_win_{i+1}") / 2.5,
                    # step_fast=3,
                    pos=(
                        dpg.get_item_pos(item="power_win_1")[0] // 2
                        - dpg.get_item_width(item=f"power_win_{i+1}") / 1.8,
                        ROW_HEIGHT // 2 - 15,
                    ),
                )

                # Indicate power as queried from the device
                dpg.add_text(
                    default_value="",
                    tag=f"power_{i+1}_indicator",
                    pos=(dpg.get_item_width(item=f"power_{i+1}"), 0),
                )

            # Bandwidth Channel Input
            with dpg.child_window(
                label=f"CHANNEL {i+1}",
                tag=f"bandwidth_win_{i+1}",
                pos=(
                    480,
                    ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT,
                ),  # (x, y)
                width=180,
                height=ROW_HEIGHT,
            ):
                dpg.add_input_text(
                    tag=f"bandwidth_{i+1}",
                    decimal=True,
                    # min_value=0, max_value=100,
                    # min_clamped=True, max_clamped=True,
                    width=dpg.get_item_width(item=f"bandwidth_win_{i+1}") / 2.5,
                    # step_fast=10,
                    pos=(
                        dpg.get_item_pos(item="bandwidth_win_1")[0] // 2
                        - dpg.get_item_width(item=f"bandwidth_win_{i+1}"),
                        ROW_HEIGHT // 2 - 15,
                    ),
                )

                # Indicate the bandwidth as queried from the
                # device
                dpg.add_text(
                    default_value="",
                    tag=f"bandwidth_{i+1}_indicator",
                    pos=(dpg.get_item_width(item=f"bandwidth_{i+1}") / 0.9, 0),
                )

            # Send Button Column
            with dpg.child_window(
                pos=(660, ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT),
                width=(200),
                height=ROW_HEIGHT,
            ):
                # SEND Buttons
                dpg.add_button(
                    label="SEND",
                    tag=f"send_btn_{i+1}",
                    height=50,
                    width=70,
                    callback=lambda: print("send button pressed"),
                    user_data=i + 1,
                    pos=(110, ROW_HEIGHT // 2 - 25),
                )

                # Status LED Buttons
                dpg.add_button(
                    tag=f"stats_{i+1}",
                    width=30,
                    height=30,
                    pos=(30, 25),
                    enabled=True,
                    callback=lambda: print("status button pressed"),
                    user_data=i + 1,
                )

                dpg.bind_item_theme(
                    item=f"row_{i+1}",
                    theme=grey_column_theme,
                )

        ########################
        # Auto Fill button row #
        ########################
        with dpg.child_window(
            pos=(80,),
            tag="auto_fill",
            height=65,
            width=200 * 3,
            border=False,
        ):
            dpg.add_button(
                label="AUTO\nFILL",
                tag="auto_fill_frequency",
                height=50,
                width=70,
                callback=lambda: print("auto fill frequency button pressed"),
                pos=(
                    dpg.get_item_width(item="auto_fill") / 9,
                    dpg.get_item_height(item="auto_fill") / 3 - 10,
                ),
            )

            dpg.add_button(
                label="AUTO\nFILL",
                tag="auto_fill_power",
                height=50,
                width=70,
                callback=lambda: print("Auto fill button pressed"),
                pos=(
                    dpg.get_item_width(item="auto_fill") / 2.2,
                    dpg.get_item_height(item="auto_fill") / 3 - 10,
                ),
            )

            dpg.add_button(
                label="AUTO\nFILL",
                tag="auto_fill_bandwidth",
                height=50,
                width=70,
                callback=lambda: print("Auto fill button pressed"),
                pos=(
                    dpg.get_item_width(item="auto_fill") / 1.3,
                    dpg.get_item_height(item="auto_fill") / 3 - 10,
                ),
            )

        _ = [
            (
                dpg.bind_item_theme(item=f"send_btn_{i+1}", theme=blue_btn_theme),
                dpg.bind_item_theme(item=f"stats_{i+1}", theme=grey_btn_theme),
            )
            for i in range(8)
        ]  # Propgation loop; Start the GUI w/ the indicator
        # buttons grey

        ##################
        # ACTION BUTTONS #
        ##################
        with dpg.child_window(
            pos=(680,),
            tag="device_config",
            border=False,
            width=200,
            height=100,
        ):
            device_config = dpg.add_button(
                label="DEVICE CONFIG",
                tag="device_config_btn",
                pos=(0,),
            )

            # Add refresh button
            dpg.add_button(
                parent="device_config",
                label="REFRESH",
                tag="refresh_devices",
                callback=lambda: print("refresh button pressed"),
                pos=(0, 70),
            )

            with dpg.popup(
                parent=device_config,
                mousebutton=dpg.mvMouseButton_Left,
                modal=True,
                tag="modal_device_config",
                no_move=True,
            ):
                try:
                    # Grab the list of Teensy devices connected
                    devices: dict[str, str] = return_teensy(device_names())

                    # Show the Serial Number to the user
                    if len(devices) == 1:
                        # Get the serial number of the device
                        # directly
                        dpg.add_menu_item(
                            label=f"{devices.popitem()[0].upper()}",
                        )

                    elif len(devices) > 1:
                        _ = [
                            (
                                dpg.add_menu_item(
                                    label=f"{device}",
                                    callback=device_finder,
                                    user_data=device,
                                ),
                            )
                            for device in devices
                        ]
                    else:
                        pass  # Error handled elsewhere

                    dpg.add_text(
                        parent="device_config",
                        tag="device_indicator",
                        default_value="Device: "
                        f"{list(return_teensy(device_names()).keys())[0]}",
                        pos=(5, 35),
                    )

                except (  # This ridiculousness is to allow the GUI to
                    TypeError,  # launch w/o a device connected
                    NameError,
                    KeyError,
                    SystemError,
                    ValueError,
                    StopIteration,
                    IndexError,
                ):
                    dpg.add_menu_item(
                        parent="choose_device",
                        label="DEVICE NUMBER: NOT FOUND",
                        callback=lambda: dpg.configure_item(
                            item="modal_device_config", show=False
                        ),
                    )
                    print("No device detected")

                    _ = [
                        dpg.bind_item_theme(
                            item=f"stats_{channel}",
                            theme=red_btn_theme,
                        )
                        for channel in range(1, 9)
                    ]
                    dpg.add_text(
                        parent="device_config",
                        tag="device_indicator",
                        default_value="",
                        pos=(5, 35),
                    )

        ################
        # Side buttons #
        ################
        with dpg.child_window(
            pos=(860, 0),
            tag="big_buttons",
            width=290,
            height=dpg.get_item_height(item="Primary Window") // 1.72,
            no_scrollbar=True,
            border=False,
        ):
            ####################
            # Stop All button #
            ####################
            print("Stop ALL button initialized")
            reset_all = dpg.add_button(
                tag="Stop_all_channels",
                height=85,
                width=BUTTON_WIDTH,
                # callback=reset_button,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - SEND_RESET_ALL_HEIGHT)
                    / 2,
                ),
            )

            dpg.add_text(
                default_value="STOP\nALL",
                pos=(
                    (dpg.get_item_width(item="big_buttons") + 10) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - SEND_RESET_ALL_HEIGHT)
                    / 2
                    + 20,
                ),
                color=(0, 0, 0, 255),
            )

            ###################
            # Send All button #
            ###################
            print("SEND ALL button initialized")
            send_all = dpg.add_button(
                tag="Send All",
                height=85,
                width=BUTTON_WIDTH,
                callback=lambda: print("Send all button pressed"),
                user_data=(
                    activate_wifi_chase,
                    bluetooth_defeat,
                ),
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 260) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - SEND_RESET_ALL_HEIGHT)
                    / 2,
                ),
            )

            dpg.add_text(
                default_value="SEND\nALL",
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 200) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - SEND_RESET_ALL_HEIGHT)
                    / 2
                    + 20,
                ),
                color=(0, 0, 0, 255),
            )

            #####################
            # Quick Save button #
            #####################
            print("Quick save button initialized")
            save_all = dpg.add_button(
                tag="save button",
                callback=lambda: print("quick save button pressed"),
                label="QUICK\n SAVE",
                height=70,
                width=BUTTON_WIDTH,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - QUICK_CONFIG_HEIGHT) / 2,
                ),
            )

            #####################
            # Quick Load button #
            #####################
            print("Quick Load button initialized")
            quick__load = dpg.add_button(
                tag="quick_load",
                callback=lambda: print("quick load button pressed"),
                label="QUICK\n LOAD",
                height=70,
                width=BUTTON_WIDTH,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - QUICK_CONFIG_HEIGHT) / 2,
                ),
            )

            ###############
            # Custom save #
            ###############
            print("Custom Save button initialized")
            custom_save_button = dpg.add_button(
                tag="custom_save",
                height=70,
                label="SAVE\nCONFIG",
                width=BUTTON_WIDTH,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - CUSTOM_CONFIG_HEIGHT)
                    / 2,
                ),
            )

            with dpg.popup(
                parent=custom_save_button,
                mousebutton=dpg.mvMouseButton_Left,
                modal=True,
                tag="modal_save",
            ):
                dpg.add_input_text(
                    # label="SAVE NAME: ",
                    tag="save_custom_input",
                    callback=lambda: print("custom save button pressed"),
                    on_enter=True,
                )
                dpg.add_button(
                    label="SAVE",
                    tag="save_button",
                    callback=lambda: print("save button pressed"),
                )

            ###############
            # Custom load #
            ###############
            print("Custom Load button initialized")

            custom_load_button = dpg.add_button(
                tag="custom_load_button",
                callback=lambda: print("custom load button pressed"),
                height=70,
                width=BUTTON_WIDTH,
                label="LOAD\nCONFIG",
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - CUSTOM_CONFIG_HEIGHT)
                    / 2,
                ),
            )

            ############################
            # Delete Saved Item button #
            ############################
            dpg.add_button(
                parent="delete_buttons",
                label="DELETE",
                callback=lambda: print("delete button pressed"),
                tag="delete_button",
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 10) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + (330 - 480)) / 2,
                ),
            )

            ########################
            # Auto Send All Button #
            ########################
            dpg.add_button(
                parent="big_buttons",
                label="AUTO SEND",
                callback=lambda: print("auto send button pressed"),
                tag="auto_button",
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 230) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + (330 - 480)) / 2,
                ),
            )

            ####################
            # MISSIONS SECTION #
            ####################
            dpg.add_text(
                default_value="MISSIONS",
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 120) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + (330 - 320)) / 2,
                ),
            )

            ##########################
            # Mission buttons border #
            ##########################
            with dpg.child_window(
                border=True,
                tag="mission_buttons_border",
                height=330,
                width=BUTTON_WIDTH * 2 + 23,
                no_scrollbar=True,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 255) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + (330 - 270)) / 2,
                ),
            ):
                ########################
                # Mission Alpha button #
                ########################
                print("Alpha button initialized")
                mission_alpha_button = dpg.add_button(
                    tag="Alpha\nConfig",
                    height=70,
                    width=BUTTON_WIDTH,
                    callback=lambda: print("Alpha button pressed"),
                    label="GPS",
                    pos=(
                        (dpg.get_item_width(item="big_buttons") - 285) / DIVISOR,
                        (dpg.get_item_height(item="big_buttons") + (DEMO_HEIGHT - 250))
                        / 2,
                    ),
                )

                ########################
                # Mission Bravo button #
                ########################
                print("Bravo button initialized")
                mission_bravo_button = dpg.add_button(
                    tag="Bravo\nConfig",
                    height=70,
                    width=BUTTON_WIDTH,
                    callback=lambda: print("Bravo button pressed"),
                    label="ZWAVE",
                    enabled=True,
                    pos=(
                        (dpg.get_item_width(item="big_buttons") - 85) / DIVISOR,
                        (dpg.get_item_height(item="big_buttons") + (DEMO_HEIGHT - 250))
                        / 2,
                    ),
                )

                ##########################
                # Mission Charlie button #
                ##########################
                print("Mission Charlie button initialized")
                mission_charlie_button = dpg.add_button(
                    tag="Charlie\nConfig",
                    callback=lambda: print("Charlie button pressed"),
                    label="DECT",
                    enabled=True,
                    height=70,
                    width=BUTTON_WIDTH,
                    pos=(
                        (dpg.get_item_width(item="big_buttons") - 285) / DIVISOR,
                        (dpg.get_item_height(item="big_buttons") + CELLUAR_HEIGHT) / 2,
                    ),
                )

                ########################
                # Mission Delta button #
                ########################
                print("Mission Delta button initialized")
                mission_delta_button = dpg.add_button(
                    tag="Delta\nConfig",
                    callback=lambda: print("Delta button pressed"),
                    label="ZIGBEE",
                    enabled=True,
                    height=70,
                    width=BUTTON_WIDTH,
                    pos=(
                        (dpg.get_item_width(item="big_buttons") - 85) / DIVISOR,
                        (dpg.get_item_height(item="big_buttons") + CELLUAR_HEIGHT) / 2,
                    ),
                )

                #################
                # SAT PHONE JAM #
                #################
                print("Mission Echo button initialized")
                mission_echo_button = dpg.add_button(
                    tag="Echo\nConfig",
                    callback=lambda: print("Echo button pressed"),
                    label="SATPHONE",
                    enabled=True,
                    height=70,
                    width=BUTTON_WIDTH,
                    pos=(
                        (dpg.get_item_width(item="big_buttons") - 285) / DIVISOR,
                        (dpg.get_item_height(item="big_buttons") + WIFI_HEIGHT) / 2,
                    ),
                )

                ###########
                # ISM JAM #
                ###########
                print("Mission Fox button initialized")
                mission_fox_button = dpg.add_button(
                    tag="Fox\nConfig",
                    callback=lambda: print("Fox button pressed"),
                    label="ISM",
                    enabled=True,
                    height=70,
                    width=BUTTON_WIDTH,
                    pos=(
                        (dpg.get_item_width(item="big_buttons") - 85) / DIVISOR,
                        (dpg.get_item_height(item="big_buttons") + WIFI_HEIGHT) / 2,
                    ),
                )

                ###############
                # Tracker Tag #
                ###############
                print("Bluetooth scan button initialized")
                mission_golf_button = dpg.add_button(
                    tag="mssn_bluetooth_scan",
                    callback=lambda: print("Bluetooth scan button pressed"),
                    label=" TRACKER \n   TAG",
                    height=70,
                    width=BUTTON_WIDTH,
                    pos=(
                        (dpg.get_item_width(item="big_buttons") - 285) / DIVISOR,
                        (dpg.get_item_height(item="big_buttons") - 480),
                    ),
                )

                ################################
                # Mission Wifi Scan Jam preset #
                ################################
                print("Mission WiFi scan jam button initialized")
                wifi_scan_jam_button = dpg.add_button(
                    tag="mssn_scan_jam",
                    callback=lambda: print("WiFi scan jam button pressed"),
                    user_data=True,
                    label="WIFI",
                    height=70,
                    width=BUTTON_WIDTH,
                    pos=(
                        (dpg.get_item_width(item="big_buttons") - 85) / DIVISOR,
                        (dpg.get_item_height(item="big_buttons") - 480),
                    ),
                )

        ##########################
        # Card Selection Buttons #
        ##########################
        with dpg.child_window(
            tag="card_presets",
            height=RESOLUTION[1] - 50,
            width=70,
            no_scrollbar=True,
            pos=(
                RESOLUTION[0] - 86,
                10,
            ),
            border=False,
        ):
            _ = [
                (
                    dpg.add_button(
                        label=f"CARD {card}",
                        tag=f"card_{card}",
                        height=60,
                        width=65,
                        pos=(0, 85 * card - 72),
                        callback=card_selection,
                        user_data=card,
                        enabled=bool(exists),
                    ),
                    dpg.bind_item_theme(item=f"card_{card}", theme=blue_btn_theme),
                )
                for card, exists in enumerate(populate_right_side_buttons(), start=1)
            ]

            with dpg.popup(
                tag="card_popup",
                parent="card_1",
                modal=True,
                mousebutton=dpg.mvMouseButton_Right,
            ):
                _ = [
                    (
                        # Input text, if the card exists, to
                        # change the name of the card
                        dpg.add_input_text(
                            label=f"Card {card} Name",
                            tag=f"card_{card}_input",
                            default_value=f"card_{card}",
                            callback=change_card_name,
                            width=200,
                            on_enter=True,
                        ),
                    )
                    for card, exists in enumerate(
                        populate_right_side_buttons(), start=1
                    )
                ]

                # Add an exit button to the popup
                dpg.add_button(
                    label="Close",
                    callback=lambda: dpg.configure_item(
                        item="card_popup",
                        show=False,
                    ),
                )

            match dpg.does_item_exist(item="card_1"):
                case False:
                    dpg.add_button(
                        label="N\nO\n\n\
    D\n E\n V\n I\n C\n E\n S\n\n  D\n  E\n  T\n  E\n  C\n  T\n  E\n  D",
                        tag="card_10",
                        height=RESOLUTION[1] - 50,
                        width=65,
                        pos=(0, 0),
                        # callback=card_selection,
                        user_data=10,
                        enabled=True,
                    )
                    dpg.bind_item_theme(item="card_10", theme=red_btn_theme)

                    dpg.configure_item(
                        item="card_0",
                        show=False,
                    )

                # If the serial number of the initially selected
                # device matches the serial number of the card 1
                # device, as set from the config file, then set
                # the theme of card 1 to green, otherwise set it
                # to blue.
                case True:
                    try:
                        dpg.bind_item_theme(
                            item="card_1", theme=grn_btn_theme
                        ) if compare_device_serial_to_config(
                            serial_num=str(return_teensy(device_names()).popitem()[0])
                        ) else dpg.bind_item_theme(
                            item="card_1", theme=grn_btn_theme
                        )
                    except KeyError:
                        print("No devices detected, disabling card 1")

        ###############
        # Version Tag #
        ###############

        with dpg.child_window(
            tag="version",
            height=20,
            width=80,
            border=False,
            no_scrollbar=True,
            pos=(
                RESOLUTION[0] - 90,
                RESOLUTION[1] - 30,
            ),
        ):
            dpg.add_button(
                label=f"ver. {__version__}",
                tag="ver_num",
                callback=tooltips,
                height=20,
                width=80,
            )

    try:  # Stop gap in case the font files cannot be found
        dpg.bind_font(font=ital_font)
        dpg.bind_item_font(item="ver_num", font=small_font)

        _ = [
            (
                dpg.bind_item_font(item=f"freq_{i}", font=bold_font),
                dpg.bind_item_font(item=f"power_{i}", font=bold_font),
                dpg.bind_item_font(item=f"bandwidth_{i}", font=bold_font),
                dpg.bind_item_font(item=f"channel_{i}", font=default_font_added),
            )
            for i in range(1, 9)
        ]

    except SystemError:
        print("Font files error")

    # Get the start up state of the card start_up_card_state()

    # Handler Registry
    # with dpg.handler_registry():
    # dpg.add_mouse_drag_handler(callback=mouse_drag_callback)
    # dpg.add_mouse_click_handler(callback=mouse_click_handler)

    # Global Theme
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
            )

        with dpg.theme_component(dpg.mvInputInt):
            dpg.add_theme_style(
                dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
            )

    # Button colors and global theme
    blue_btn_list: list[Any] = [
        save_all,
        quick__load,
        custom_save_button,
        mission_golf_button,
        mission_alpha_button,
        custom_load_button,
        mission_bravo_button,
        mission_charlie_button,
        mission_delta_button,
        mission_echo_button,
        mission_fox_button,
        wifi_scan_jam_button,
    ]

    dpg.bind_theme(global_theme)

    _ = [
        dpg.bind_item_theme(
            item=btn,
            theme=blue_btn_theme,
        )
        for btn in blue_btn_list
    ]
    dpg.bind_item_theme(item=send_all, theme=grn_btn_theme)
    dpg.bind_item_theme(item=reset_all, theme=red_btn_theme)


##################################
# TESTS ASSOCIATED WITH FIXTURES #
##################################

""" MISSION GUI BUTTON TESTS """


def test_alpha_gui_button_is_created(dpg_complex_context):
    assert dpg.does_item_exist(item="Alpha\nConfig")


def test_bravo_gui_button_is_created(dpg_complex_context):
    assert dpg.does_item_exist(item="Bravo\nConfig")


def test_charlie_gui_button_is_created(dpg_complex_context):
    assert dpg.does_item_exist(item="Charlie\nConfig")


def test_delta_gui_button_is_created(dpg_complex_context):
    assert dpg.does_item_exist(item="Delta\nConfig")


def test_echo_gui_button_is_created(dpg_complex_context):
    assert dpg.does_item_exist(item="Echo\nConfig")


def test_fox_gui_button_is_created(dpg_complex_context):
    assert dpg.does_item_exist(item="Fox\nConfig")


def test_bluetooth_button_is_created(dpg_complex_context):
    assert dpg.does_item_exist(item="mssn_bluetooth_scan")


def test_wifi_button_is_created(dpg_complex_context):
    assert dpg.does_item_exist(item="mssn_scan_jam")


""" GUI BUTTON ENABLED TESTS """


def test_is_alpha_gui_button_enabled(dpg_complex_context):
    assert dpg.is_item_enabled(item="Alpha\nConfig")


def test_is_bravo_gui_button_enabled(dpg_complex_context):
    assert dpg.is_item_enabled(item="Bravo\nConfig")


def test_is_charlie_gui_button_enabled(dpg_complex_context):
    assert dpg.is_item_enabled(item="Charlie\nConfig")


def test_is_delta_gui_button_enabled(dpg_complex_context):
    assert dpg.is_item_enabled(item="Delta\nConfig")


def test_is_echo_gui_button_enabled(dpg_complex_context):
    assert dpg.is_item_enabled(item="Echo\nConfig")


def test_is_fox_gui_button_enabled(dpg_complex_context):
    assert dpg.is_item_enabled(item="Fox\nConfig")


def test_is_bluetooth_button_enabled(dpg_complex_context):
    assert dpg.is_item_enabled(item="mssn_bluetooth_scan")


def test_is_wifi_button_enabled(dpg_complex_context):
    assert dpg.is_item_enabled(item="mssn_scan_jam")


""" GUI BUTTON DISABLED TESTS """


def test_is_alpha_gui_button_disabled(dpg_complex_context):
    dpg.disable_item(item="Alpha\nConfig")
    assert dpg.is_item_enabled(item="Alpha\nConfig") == False


def test_is_bravo_gui_button_disabled(dpg_complex_context):
    dpg.disable_item(item="Bravo\nConfig")
    assert dpg.is_item_enabled(item="Bravo\nConfig") == False


def test_is_charlie_gui_button_disabled(dpg_complex_context):
    dpg.disable_item(item="Charlie\nConfig")
    assert dpg.is_item_enabled(item="Charlie\nConfig") == False


def test_is_delta_gui_button_disabled(dpg_complex_context):
    dpg.disable_item(item="Delta\nConfig")
    assert dpg.is_item_enabled(item="Delta\nConfig") == False


def test_is_echo_gui_button_disabled(dpg_complex_context):
    dpg.disable_item(item="Echo\nConfig")
    assert dpg.is_item_enabled(item="Echo\nConfig") == False


def test_is_fox_gui_button_disabled(dpg_complex_context):
    dpg.disable_item(item="Fox\nConfig")
    assert dpg.is_item_enabled(item="Fox\nConfig") == False


def test_is_bluetooth_button_disabled(dpg_complex_context):
    dpg.disable_item(item="mssn_bluetooth_scan")
    assert dpg.is_item_enabled(item="mssn_bluetooth_scan") == False


def test_is_wifi_button_disabled(dpg_complex_context):
    dpg.disable_item(item="mssn_scan_jam")
    assert dpg.is_item_enabled(item="mssn_scan_jam") == False


""" DELETE THEN TEST GUI BUTTON TESTS """


def test_delete_alpha_button(dpg_complex_context):
    if dpg.does_item_exist(item="Alpha\nConfig"):
        dpg.delete_item(item="Alpha\nConfig")
        assert dpg.does_item_exist(item="Alpha\nConfig") == False


def test_delete_bravo_button(dpg_complex_context):
    if dpg.does_item_exist(item="Bravo\nConfig"):
        dpg.delete_item(item="Bravo\nConfig")
        assert dpg.does_item_exist(item="Bravo\nConfig") == False


def test_delete_charlie_button(dpg_complex_context):
    if dpg.does_item_exist(item="Charlie\nConfig"):
        dpg.delete_item(item="Charlie\nConfig")
        assert dpg.does_item_exist(item="Charlie\nConfig") == False


def test_delete_delta_button(dpg_complex_context):
    if dpg.does_item_exist(item="Delta\nConfig"):
        dpg.delete_item(item="Delta\nConfig")
        assert dpg.does_item_exist(item="Delta\nConfig") == False


def test_echo_alpha_button(dpg_complex_context):
    if dpg.does_item_exist(item="Echo\nConfig"):
        dpg.delete_item(item="Echo\nConfig")
        assert dpg.does_item_exist(item="Echo\nConfig") == False


###########################
# GENERAL GUI BUTTON TEST #
###########################

""" GUI BUTTON TESTS (NON_MISSION) """

for i in range(1, 9):

    def test_are_send_buttons_created(dpg_complex_context):
        for x in range(1, 9):
            assert dpg.does_item_exist(item=f"send_btn_{i}")


# def test_alpha_gui_button_color(dpg_complex_context):
# color = dpg.get_item_theme(item="Alpha\nConfig")
# with dpg.theme() as blue_btn_theme:
# with dpg.theme_component(dpg.mvAll):
# dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))
# assert color == blue_btn_theme
