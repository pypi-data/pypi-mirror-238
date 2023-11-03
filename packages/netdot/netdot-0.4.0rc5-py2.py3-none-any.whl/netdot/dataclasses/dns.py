from dataclasses import dataclass

from netdot import parse
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass


@dataclass
class Zone(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Zone"

    active: bool = False
    contactlist: str = None
    contactlist_xlink: int = None
    expire: int = None
    info: str = None
    minimum: int = None
    name: str = None
    refresh: int = None
    retry: int = None
    rname: str = None
    serial: int = None
    default_ttl: int = None
    export_file: str = None
    mname: str = None
    include: str = None


@dataclass
class ZoneAlias(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "dns"
    NETDOT_TABLE_NAME = "ZoneAlias"

    info: str = None
    name: str = None
    zone: str = None
    zone_xlink: int = None


@dataclass
class RR(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RR"
    # TODO the web_url is actually 'host' -- need to add another class variable for 'NETDOT_MENU_URL_PATH'

    active: bool = False
    auto_update: bool = False
    expiration: parse.DateTime = None
    info: str = None
    name: str = None
    zone: str = None
    zone_xlink: int = None
    created: parse.DateTime = None
    modified: parse.DateTime = None


@dataclass
class RRADDR(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RRADDR"

    ipblock: str = None
    ipblock_xlink: int = None
    rr: str = None
    rr_xlink: int = None
    ttl: str = None


@dataclass
class RRCNAME(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RRCNAME"

    cname: str = None
    rr: str = None
    rr_xlink: int = None
    ttl: str = None


@dataclass
class RRDS(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RRDS"

    algorithm: int = None
    digest: str = None
    digest_type: int = None
    key_tag: int = None
    rr: str = None
    rr_xlink: int = None
    ttl: str = None


@dataclass
class RRHINFO(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RRHINFO"

    cpu: str = None
    os: str = None
    rr: str = None
    rr_xlink: int = None
    ttl: str = None


@dataclass
class RRLOC(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RRLOC"

    altitude: int = None
    horiz_pre: str = None
    latitude: str = None
    longitude: str = None
    rr: str = None
    rr_xlink: int = None
    size: str = None
    ttl: str = None
    vert_pre: str = None


@dataclass
class RRMX(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RRMX"

    exchange: str = None
    preference: int = None
    rr: str = None
    rr_xlink: int = None
    ttl: str = None


@dataclass
class RRNAPTR(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RRNAPTR"

    flags: str = None
    order_field: int = None
    preference: int = None
    regexpr: str = None
    replacement: str = None
    rr: str = None
    rr_xlink: int = None
    services: str = None
    ttl: str = None


@dataclass
class RRNS(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RRNS"

    nsdname: str = None
    rr: str = None
    rr_xlink: int = None
    ttl: str = None


@dataclass
class RRPTR(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "RRPTR"

    ipblock: str = None
    ipblock_xlink: int = None
    ptrdname: str = None
    rr: str = None
    rr_xlink: int = None
    ttl: str = None


@dataclass
class RRSRV(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "dns"
    NETDOT_TABLE_NAME = "RRSRV"

    port: int = None
    priority: int = None
    rr: str = None
    rr_xlink: int = None
    target: str = None
    ttl: str = None
    weight: int = None


@dataclass
class RRTXT(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "dns"
    NETDOT_TABLE_NAME = "RRTXT"

    rr: str = None
    rr_xlink: int = None
    ttl: str = None
    txtdata: str = None
