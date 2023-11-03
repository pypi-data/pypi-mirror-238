from dataclasses import dataclass
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass
import ipaddress
from netdot import parse


@dataclass
class Availability(NetdotAPIDataclass, CSVDataclass):
    """Contains a description of some availability status. Examples: 24x7, 800-1700, 700-2200."""

    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Availability"

    info: str = None
    name: str = None


# TODO Netdot REST API seems to not return blob data
# @dataclass
# class DataCache(NetdotAPIDataclass, CSVDataclass):
#     NETDOT_MENU_URL_PATH = "management"
#     NETDOT_TABLE_NAME = "DataCache"

#     data: str = None
#     name: str = None
#     tstamp: int = None


@dataclass
class HostAudit(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "HostAudit"

    tstamp: parse.DateTime = None
    zone: str = None
    scope: str = None
    pending: bool = False


@dataclass
class MaintContract(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "MaintContract"
    _xlink_class_map = {"provider": "Entity"}

    info: str = None
    number: str = None
    provider: str = None
    provider_xlink: int = None


@dataclass
class MonitorStatus(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "MonitorStatus"

    info: str = None
    name: str = None


@dataclass
class SavedQueries(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "SavedQueries"

    name: str = None
    querytext: str = None


@dataclass
class SchemaInfo(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "SchemaInfo"

    info: str = None
    version: str = None
