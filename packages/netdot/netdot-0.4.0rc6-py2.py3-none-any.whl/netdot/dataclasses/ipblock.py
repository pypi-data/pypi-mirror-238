import ipaddress
import logging
from dataclasses import dataclass
from typing import List

from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass
from netdot import parse

logger = logging.getLogger(__name__)


@dataclass
class IPBlock(NetdotAPIDataclass, CSVDataclass):
    """Represents either a subnet or an individual address.
    """
    # TODO: consider making aliases for this class: IPContainer IPAddress, IPSubnet

    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Ipblock"
    _xlink_class_map = {
        "parent_xlink": "IPBlock",
        "owner": "Entity",
        "used_by": "Entity",
        "status": "IPBlockStatus",
    }

    address: ipaddress.ip_address = None
    description: str = None
    first_seen: parse.DateTime = None
    info: str = None
    interface: str = None
    interface_xlink: int = None
    last_seen: parse.DateTime = None
    owner: str = None
    owner_xlink: int = None
    parent: str = None
    parent_xlink: int = None
    prefix: int = None
    status: str = None
    status_xlink: int = None
    used_by: str = None
    used_by_xlink: int = None
    version: int = None
    vlan: str = None
    vlan_xlink: int = None
    use_network_broadcast: bool = False
    monitored: bool = False
    rir: str = None
    asn: str = None
    asn_xlink: int = None
    _parent: List["IPBlock"] = None

    def get_parent(self) -> "IPBlock":
        """Get the parent of this IPBlock.

        Returns:
            IPBlock: The parent of this IPBlock.

        Raises:
            HTTPError: If no results found.
        """
        if self._parent is None:
            self._parent = self.repository.get_ipblock(self.parent_xlink)
        return self._parent

    def get_children(self) -> List["IPBlock"]:
        """Get the children of this IPBlock.

        Returns:
            List[IPBlock]: The children of this IPBlock.

        Raises:
            HTTPError: If no results found.
        """
        return self.repository.get_ipblock_children(self.id)


@dataclass
class IPBlockAttrName(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "IpblockAttrName"

    info: str = None
    name: str = None


@dataclass
class IPBlockStatus(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "IpblockStatus"

    name: str = None


@dataclass
class Service(NetdotAPIDataclass, CSVDataclass):
    """Network services, such as: NTP, POP3, RADIUS, SMTP, SSH, TELNET..."""

    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Service"

    info: str = None
    name: str = None


@dataclass
class IPBlockAttr(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "IpblockAttr"

    ipblock: str = None
    ipblock_xlink: int = None
    name: str = None
    name_xlink: int = None
    value: str = None


@dataclass
class IPService(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "IpService"
    _xlink_class_map = {
        "ip": "Ipblock",
    }
    contactlist: str = None
    contactlist_xlink: int = None
    ip: str = None
    ip_xlink: int = None
    monitored: bool = False
    monitorstatus: str = None
    monitorstatus_xlink: int = None
    service: str = None
    service_xlink: int = None


@dataclass
class SubnetZone(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "SubnetZone"

    subnet: str = None
    subnet_xlink: int = None
    zone: str = None
    zone_xlink: int = None
