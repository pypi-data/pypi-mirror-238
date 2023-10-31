"""Algorithm that continuosly scans and chases an SSID."""

from dataclasses import dataclass


@dataclass
class Chasing:
    """Algorithm that continuosly scans and chases an SSID."""

    ssid: str
    channel: int
    prev_freq: float
    present_freq: float
    port: int = 8081

    def __post_init__(self):
        """Initialize the algorithm."""
        self.prev_freq = 0
        self.present_freq = 0

    def initiate_scan(self, interface):
        """Initiate a scan."""
        interface.scan()
