import logging
from dataclasses import dataclass
from datetime import datetime

from netdot import parse
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass
from netdot.mac_address import MACAddress

logger = logging.getLogger(__name__)


@dataclass
class FWTable(NetdotAPIDataclass, CSVDataclass):
    """Forwarding Table for a device."""

    NETDOT_MENU_URL_PATH = 'management'
    NETDOT_TABLE_NAME = 'FWTable'
    device: str = None
    device_xlink: int = None
    id: int = None
    tstamp: parse.DateTime = None


@dataclass
class FWTableEntry(NetdotAPIDataclass, CSVDataclass):
    """Forwarding Table entries."""

    NETDOT_MENU_URL_PATH = 'generic'
    NETDOT_URL_PATH = 'fwtableentry'
    NETDOT_TABLE_NAME = 'FWTableEntry'
    fwtable: str = None
    fwtable_xlink: int = None
    id: int = None
    interface: str = None
    interface_xlink: int = None
    physaddr: MACAddress = None
    physaddr_xlink: int = None

    def infer_timestamp(self) -> datetime:
        """Infer the timestamp of this FWTableEntry (based on the 'fwtable' string returned to us by Netdot API).

        Returns:
            datetime: The inferred timestamp.

        Raises:
            ValueError: If unable to infer the timestamp.
        """
        try:
            tokens = parse.split_combined_entities_str(self.fwtable)
            if len(tokens) == 2:
                return parse.DateTime(tokens[0])
        except Exception:
            raise ValueError(f'Unsure how to parse timestamp from fwtable string: {self.fwtable}')
 