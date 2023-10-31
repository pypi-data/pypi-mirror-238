from pathlib import Path
import pytest
from ..gui.helpers import convert_power
from ..gui.helpers import kill_channel
from ..globals.helpers import version_getter

scan_results: dict = {}  # find_signals_and_frequencies()

test_db_path: str | Path = Path("test.db")


def test_kill_channel() -> None:
    assert kill_channel.__name__


@pytest.mark.skip
def test_wifi_scanner():
    assert isinstance(scan_results, dict)


@pytest.mark.skip
def test_frequency_and_signal_value_exists():
    x = scan_results
    assert len(x) != 0, "Dictionary should not be empty"


@pytest.mark.skip
def test_frequency_for_string():
    assert "Infra" not in scan_results.items()


@pytest.mark.skip
def test_frequency_value():
    assert 2412 or 5220 in scan_results.values()


@pytest.mark.skip
def test_frequency_value2():
    assert 2437 or 2462 in scan_results.values()


@pytest.mark.skip
def test_signal_string():
    assert "MHz" not in scan_results


@pytest.mark.skip
def test_version_getter():
    assert isinstance(version_getter(), str)


@pytest.mark.skip
def test_version_are_numbers():
    # parse the version string
    version: str = str(version_getter())
    version = version.split(".")  # type: ignore

    # check if the version is a number
    assert version[0].isdigit()
    assert version[1].isdigit()
    assert version[2].isdigit()


def test_convert_power_min():
    assert convert_power(power=0) == 0


def test_convert_power_max():
    assert convert_power(power=100) == 63


def test_convert_power_mid():
    assert convert_power(power=50) == 32


def test_convert_power_mid2():
    assert convert_power(power=25) == 16


def test_convert_power_mid3():
    assert convert_power(power=75) == 47
