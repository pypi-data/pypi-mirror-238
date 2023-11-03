import logging
from dataclasses import dataclass

from netdot import parse
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass

logger = logging.getLogger(__name__)


@dataclass
class ContactList(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "ContactList"

    info: str = None
    name: str = None


@dataclass
class ContactType(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "ContactType"

    info: str = None
    name: str = None


@dataclass
class AccessRight(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "AccessRight"

    access: str = None
    object_class: str = None
    object_id: int = None


@dataclass
class GroupRight(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "GroupRight"
    _associative_table = True

    accessright: str = None
    accessright_xlink: int = None
    contactlist: str = None
    contactlist_xlink: int = None


@dataclass
class Audit(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Audit"

    fields: str = None
    label: str = None
    object_id: int = None
    operation: str = None
    tablename: str = None
    tstamp: parse.DateTime = None
    username: str = None
    vals: str = None


@dataclass
class UserType(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "UserType"

    info: str = None
    name: str = None


@dataclass
class Person(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Person"
    _xlink_class_map = {
        "location": "Site",
        "user_type": "UserType",
    }

    aliases: str = None
    cell: str = None
    email: str = None
    emailpager: str = None
    entity: str = None
    entity_xlink: int = None
    extension: int = None
    fax: str = None
    firstname: str = None
    home: str = None
    info: str = None
    lastname: str = None
    location: str = None
    location_xlink: int = None
    office: str = None
    pager: str = None
    position: str = None
    room: str = None
    room_xlink: int = None
    user_type: str = None
    user_type_xlink: int = None
    username: str = None
    password: str = None  # TODO Should we use HiddenString?


@dataclass
class Contact(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Contact"
    _xlink_class_map = {
        "notify_pager": "Availability",
        "notify_email": "Availability",
        "notify_voice": "Availability",
    }
    contactlist: str = None
    contactlist_xlink: int = None
    contacttype: str = None
    contacttype_xlink: int = None
    escalation_level: int = None
    info: str = None
    notify_email: str = None
    notify_email_xlink: int = None
    notify_pager: str = None
    notify_pager_xlink: int = None
    notify_voice: str = None
    notify_voice_xlink: int = None
    person: str = None
    person_xlink: int = None


@dataclass
class UserRight(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "UserRight"
    _associative_table = True

    accessright: str = None
    accessright_xlink: int = None
    person: str = None
    person_xlink: int = None
