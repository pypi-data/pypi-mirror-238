from dataclasses import dataclass

from netdot import parse
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass


@dataclass
class HorizontalCable(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "HorizontalCable"
    _xlink_class_map = {
        "type": "CableType",
    }

    account: str = None
    closet: str = None
    closet_xlink: int = None
    contactlist: str = None
    contactlist_xlink: int = None
    datetested: parse.DateTime = None
    faceplateid: str = None
    info: str = None
    installdate: parse.DateTime = None
    jackid: str = None
    length: str = None
    room: str = None
    room_xlink: int = None
    testpassed: bool = False
    type: str = None
    type_xlink: int = None


@dataclass
class BackboneCable(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "BackboneCable"
    _xlink_class_map = {
        "end_closet": "Closet",
        "owner": "Entity",
        "start_closet": "Closet",
        "type": "CableType",
    }

    end_closet: str = None
    end_closet_xlink: int = None
    info: str = None
    installdate: parse.DateTime = None
    length: str = None
    name: str = None
    owner: str = None
    owner_xlink: int = None
    start_closet: str = None
    start_closet_xlink: int = None
    type: str = None
    type_xlink: int = None


@dataclass
class Circuit(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Circuit"
    _xlink_class_map = {
        "linkid": "SiteLink",
        "status": "CircuitStatus",
        "type": "CircuitType",
        "vendor": "Entity",
    }

    cid: str = None
    info: str = None
    installdate: parse.DateTime = None
    linkid: str = None
    linkid_xlink: int = None
    speed: str = None
    status: str = None
    status_xlink: int = None
    type: str = None
    type_xlink: int = None
    vendor: str = None
    vendor_xlink: int = None
    datetested: parse.DateTime = None
    loss: str = None


@dataclass
class StrandStatus(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "StrandStatus"

    info: str = None
    name: str = None


@dataclass
class CableStrand(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "CableStrand"
    _xlink_class_map = {
        "cable": "BackboneCable",
        "fiber_type": "FiberType",
        "status": "StrandStatus",
    }

    cable: str = None
    cable_xlink: int = None
    circuit_id: str = None
    circuit_id_xlink: int = None
    description: str = None
    fiber_type: str = None
    fiber_type_xlink: int = None
    info: str = None
    name: str = None
    number: int = None
    status: str = None
    status_xlink: int = None


@dataclass
class Splice(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Splice"
    _xlink_class_map = {
        "strand1": "CableStrand",
        "strand2": "CableStrand",
    }

    info: str = None
    strand1: str = None
    strand1_xlink: int = None
    strand2: str = None
    strand2_xlink: int = None


@dataclass
class CableType(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "CableType"

    info: str = None
    name: str = None


@dataclass
class CircuitStatus(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "CircuitStatus"

    info: str = None
    name: str = None


@dataclass
class CircuitType(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "CircuitType"

    info: str = None
    name: str = None


@dataclass
class FiberType(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "FiberType"

    info: str = None
    name: str = None
