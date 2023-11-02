import logging
from dataclasses import dataclass
from typing import List

from netdot import parse
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass
from netdot.mac_address import MACAddress

logger = logging.getLogger(__name__)


def is_up(up_str: str):
    return up_str.lower().strip() == "up"


@dataclass
class Interface(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Interface"
    id: int = None
    physaddr: MACAddress = None
    physaddr_xlink: int = None
    oper_status: str = None
    admin_status: str = None
    neighbor: str = None
    admin_duplex: str = None
    admin_status: str = None
    bpdu_filter_enabled: bool = None
    bpdu_guard_enabled: bool = None
    contactlist: str = None
    contactlist_xlink: int = None
    description: str = None
    device: str = None
    device_xlink: str = None
    doc_status: str = None
    down_from: parse.DateTime = None
    down_until: parse.DateTime = None
    dp_remote_id: str = None
    dp_remote_ip: str = None
    dp_remote_port: str = None
    dp_remote_type: str = None
    info: str = None
    jack: str = None
    jack_xlink: str = None
    jack_char: str = None
    loop_guard_enabled: bool = None
    monitored: bool = None
    monitorstatus: str = None
    monitorstatus_xlink: int = None
    name: str = None
    neighbor: str = None
    neighbor_xlink: int = (
        None  # TODO, how to wire the neighbor up to look up another interface?
    )
    neighbor_fixed: bool = None
    neighbor_missed: int = None
    number: str = None
    oper_duplex: str = None
    oper_status: str = None
    overwrite_descr: bool = None
    room_char: str = None
    root_guard_enabled: bool = None
    snmp_managed: bool = None
    speed: int = None
    stp_id: str = None
    type: str = None
    ignore_ip: bool = None
    auto_dns: bool = None
    circuit: int = None
    dlci: str = None

    @property
    def oper_up(self):
        return is_up(self.oper_status)

    @property
    def admin_up(self):
        return is_up(self.admin_status)

    @property
    def is_up(self):
        """An interface is 'up' if both the 'admin' and 'oper' status are 'up'"""
        return self.oper_up and self.admin_up

    # def _is_access_port(self):
    #     """TODO Is this an access port? (best-effort, may also include non-access ports)

    #     An Access Port is one that is used by the actual access layer, e.g. desktops, servers, laptops.

    #     We determine whether this interface may be an access first by checking for the following:
    #     * a single VLAN,
    #     * named like a physical interface...* TODO

    #     Then, we can look for any signs any signs it is NOT an access port:
    #     * has a 'neighboring interface',

    #     TODO: Is this valid we have LLDP-MED access ports?
    #     """
    #     if self.neighbor is None:
    #         return False
    #     vlans = self.get_vlans()
    #     if len(vlans) != 1:
    #         return False
    #     return True


@dataclass
class InterfaceVLAN(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "InterfaceVlan"
    _xlink_class_map = {
        "stp_instance": "STPInstance",
    }
    interface: str = None
    interface_xlink: int = None
    stp_des_bridge: str = None
    stp_des_port: str = None
    stp_instance: str = None
    stp_instance_xlink: int = None
    stp_state: str = None
    vlan: str = None
    vlan_xlink: int = None
