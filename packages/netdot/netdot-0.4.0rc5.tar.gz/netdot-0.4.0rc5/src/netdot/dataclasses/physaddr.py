import logging
from dataclasses import dataclass

from netdot import parse
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass
from netdot.mac_address import MACAddress

logger = logging.getLogger(__name__)


@dataclass
class PhysAddr(NetdotAPIDataclass, CSVDataclass):
    """Represents a physical/MAC address."""

    NETDOT_TABLE_NAME = "PhysAddr"
    NETDOT_URL_PATH = "mac"
    NETDOT_MENU_URL_PATH = "management"
    # TODO Does web_url work for this class?
    id: int = None
    address: MACAddress = None
    static: bool = False
    first_seen: parse.DateTime = None
    last_seen: parse.DateTime = None


@dataclass
class PhysAddrAttrName(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "PhysAddrAttrName"

    id: int = None
    info: str = None
    name: str = None


@dataclass
class PhysAddrAttr(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "PhysAddrAttr"

    id: int = None
    name: int = None
    physaddr: int = None
    value: str = None
