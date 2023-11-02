import logging
from dataclasses import dataclass

from netdot import parse
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass
from netdot.mac_address import MACAddress

logger = logging.getLogger(__name__)


@dataclass
class BGPPeering(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "BGPPeering"

    bgppeeraddr: str = None
    bgppeerid: str = None
    device: str = None
    device_xlink: int = None
    entity: str = None
    entity_xlink: int = None
    monitored: bool = False
    authkey: str = None
    info: str = None
    max_v4_prefixes: int = None
    max_v6_prefixes: int = None
    contactlist: str = None
    contactlist_xlink: int = None
    last_changed: parse.DateTime = None
    peer_group: str = None
    state: str = None


@dataclass
class ASN(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "ASN"

    description: str = None
    info: str = None
    number: int = None
    rir: str = None
