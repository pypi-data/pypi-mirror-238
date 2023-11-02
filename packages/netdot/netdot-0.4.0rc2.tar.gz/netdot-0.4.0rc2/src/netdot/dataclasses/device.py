import ipaddress
import logging
from dataclasses import dataclass

from netdot import parse
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass

logger = logging.getLogger(__name__)


@dataclass
class Device(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_URL_PATH = "device"
    NETDOT_TABLE_NAME = "Device"
    _xlink_class_map = {
        'asset_id': 'Asset',
        'name': 'RR',
        'owner': 'Entity',
        'snmp_target': 'IPBlock',
        'used_by': 'Entity',
    }
    #
    # Relational fields
    #
    site_xlink: int = None
    site: str = None
    asset_id: str = None
    asset_id_xlink: int = None
    monitorstatus: int = None
    monitorstatus_xlink: int = None
    name: str = None
    name_xlink: int = None
    host_device: str = None
    host_device_xlink: int = None
    bgplocalas: int = None
    bgplocalas_xlink: int = None
    snmp_target: ipaddress.ip_address = None
    snmp_target_xlink: int = None
    room: str = None
    room_xlink: int = None
    owner: str = None
    owner_xlink: int = None
    used_by: str = None
    used_by_xlink: int = None
    #
    # Basic fields
    #
    id: int = None
    aliases: str = None
    bgpid: str = None
    canautoupdate: bool = None
    collect_arp: bool = None
    collect_fwt: bool = None
    collect_stp: bool = None
    community: str = None
    customer_managed: bool = None
    date_installed: parse.DateTime = None
    down_from: parse.DateTime = None
    down_until: parse.DateTime = None
    info: str = None
    ipforwarding: bool = None
    last_arp: parse.DateTime = None
    last_fwt: parse.DateTime = None
    last_updated: parse.DateTime = None
    layers: str = None
    monitor_config: bool = None
    monitor_config_group: str = None
    monitored: bool = None
    monitoring_path_cost: int = None
    oobname: str = None
    oobnumber: str = None
    os: str = None
    rack: str = None
    snmp_authkey: str = None
    snmp_authprotocol: str = None
    snmp_bulk: bool = None
    snmp_managed: bool = None
    snmp_polling: bool = None
    snmp_privkey: str = None
    snmp_privprotocol: str = None
    snmp_securitylevel: str = None
    snmp_securityname: str = None
    snmp_version: int = None
    stp_enabled: bool = None
    stp_mst_digest: str = None
    stp_mst_region: str = None
    stp_mst_rev: str = None
    stp_type: str = None
    sysdescription: str = None
    syslocation: str = None
    sysname: str = None
    auto_dns: bool = None
    extension: str = None
    snmp_conn_attempts: int = None
    snmp_down: bool = None
    oobname_2: str = None
    oobnumber_2: str = None
    power_outlet: str = None
    power_outlet_2: str = None
    monitoring_template: str = None


@dataclass
class DeviceAttr(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "DeviceAttr"
    _xlink_class_map = {
        "name": "DeviceAttrName",
    }
    device: str = None
    device_xlink: int = None
    name: str = None
    name_xlink: int = None
    value: str = None


@dataclass
class DeviceAttrName(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "DeviceAttrName"

    info: str = None
    name: str = None


@dataclass
class DeviceContacts(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "DeviceContacts"
    _associative_table = True

    contactlist: str = None
    contactlist_xlink: int = None
    device: str = None
    device_xlink: int = None


@dataclass
class DeviceModule(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "DeviceModule"

    class_: str = None
    contained_in: int = None
    date_installed: parse.DateTime = None
    description: str = None
    device: str = None
    device_xlink: int = None
    fru: bool = False
    fw_rev: str = None
    hw_rev: str = None
    last_updated: parse.DateTime = None
    model: str = None
    name: str = None
    number: int = None
    pos: int = None
    sw_rev: str = None
    type: str = None
    asset_id: str = None
    asset_id_xlink: int = None


@dataclass
class OUI(NetdotAPIDataclass, CSVDataclass):
    """Organizational Unique Identifier (OUI) is a 24-bit number that uniquely identifies a vendor or manufacturer."""

    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "OUI"

    oui: str = None
    vendor: str = None


@dataclass
class STPInstance(NetdotAPIDataclass, CSVDataclass):
    """Spanning Tree Protocol instance."""

    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "STPInstance"

    bridge_priority: int = None
    device: str = None
    device_xlink: int = None
    number: int = None
    root_bridge: str = None
    root_port: int = None
