import logging
from dataclasses import dataclass

from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass

logger = logging.getLogger(__name__)


@dataclass
class DHCPScope(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "DhcpScope"
    _xlink_class_map = {
        "container": "DHCPScope",
        "type": "DHCPScopeType",
    }
    ipblock: str = None
    ipblock_xlink: int = None
    text: str = None
    name: str = None
    container: str = None
    container_xlink: int = None
    physaddr: str = None
    physaddr_xlink: int = None
    type: str = None
    type_xlink: int = None
    export_file: str = None
    enable_failover: bool = False
    failover_peer: str = None
    active: bool = False
    duid: str = None
    version: int = None


@dataclass
class DHCPAttr(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "DhcpAttr"

    name: str = None
    name_xlink: int = None
    scope: str = None
    scope_xlink: int = None
    value: str = None


@dataclass
class DHCPScopeUse(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "DhcpScopeUse"
    _xlink_class_map = {
        "scope": "DHCPScope",
        "template": "DHCPScope",
    }

    scope: str = None
    scope_xlink: int = None
    template: str = None
    template_xlink: int = None


@dataclass
class DHCPAttrName(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "DhcpAttrName"

    code: int = None
    format: str = None
    info: str = None
    name: str = None


@dataclass
class DHCPScopeType(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "DhcpScopeType"

    info: str = None
    name: str = None
