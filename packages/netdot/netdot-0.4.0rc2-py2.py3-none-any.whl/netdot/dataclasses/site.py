# type: ignore
import logging
from dataclasses import dataclass
from typing import List

from netdot.exceptions import HTTPError
from netdot.csv_util import CSVDataclass
from netdot.dataclasses.base import NetdotAPIDataclass

logger = logging.getLogger(__name__)


@dataclass
class Site(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "cable_plant"
    NETDOT_TABLE_NAME = "Site"
    name: str = None
    aliases: str = None
    availability: str = None
    availability_xlink: int = None
    contactlist: str = None
    contactlist_xlink: int = None
    gsf: str = None
    number: str = None  # maps to GISSite `building_number` property
    street1: str = None  # First line of 'civic address'
    street2: str = None  # Optional second line of 'civic address'
    state: str = None
    city: str = None
    country: str = None
    zip: str = None
    pobox: str = None
    info: str = None

    def load_rooms(self) -> List['Room']:
        """Load all rooms for this site."""
        rooms = list()
        for floor in self.load_floors():
            rooms.extend(floor.load_rooms())
        return rooms

    def load_closets(self) -> List['Closet']:
        """Load all closets for this site.

        > NOTE: This will make N+1 HTTP Requests (where N is the number of rooms in this site).
        """
        closets = list()
        for room in self.load_rooms():
            try:
                closets.extend(room.load_closets())
            except HTTPError as e:
                if hasattr(e.response, 'status_code') and e.response.status_code == 404:
                    logger.info(f"Room {room.name} does not have any closets.")
                else:
                    raise e
        return closets


@dataclass
class SiteSubnet(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "SiteSubnet"
    _associative_table = True
    _xlink_class_map = {
        'subnet': 'IPBlock',
    }

    site: str = None
    site_xlink: int = None
    subnet: str = None
    subnet_xlink: int = None


@dataclass
class Floor(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Floor"

    info: str = None
    level: str = None
    site: str = None
    site_xlink: int = None


@dataclass
class Room(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Room"

    floor: str = None
    floor_xlink: int = None
    name: str = None


@dataclass
class Closet(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "Closet"

    access_key_type: str = None
    asbestos_tiles: bool = False
    catv_taps: str = None
    converted_patch_panels: bool = False
    dimensions: str = None
    ground_buss: bool = False
    hvac_type: str = None
    info: str = None
    name: str = None
    room: str = None
    room_xlink: int = None
    ot_blocks: str = None
    outlets: str = None
    pair_count: str = None
    patch_panels: str = None
    rack_type: str = None
    racks: str = None
    ru_avail: str = None
    shared_with: str = None
    ss_blocks: str = None
    work_needed: str = None


@dataclass
class SiteLink(NetdotAPIDataclass, CSVDataclass):
    NETDOT_MENU_URL_PATH = "management"
    NETDOT_TABLE_NAME = "SiteLink"
    _xlink_class_map = {
        "farend": "Site",
        "nearend": "Site",
    }

    entity: str = None
    entity_xlink: int = None
    farend: str = None
    farend_xlink: int = None
    info: str = None
    name: str = None
    nearend: str = None
    nearend_xlink: int = None


# TODO Netdot REST API seems to not return blob data
# @dataclass
# class SitePicture(NetdotAPIDataclass, CSVDataclass):
#     NETDOT_MENU_URL_PATH = "management"
#     NETDOT_TABLE_NAME = "SitePicture"

#     bindata: str = None
#     filename: str = None
#     filesize: str = None
#     filetype: str = None
#     info: str = None
#     site: str = None
#     site_xlink: int = None


# TODO Netdot REST API seems to not return blob data
# @dataclass
# class FloorPicture(NetdotAPIDataclass, CSVDataclass):
#     NETDOT_MENU_URL_PATH = "management"
#     NETDOT_TABLE_NAME = "FloorPicture"

#     bindata: str = None
#     filename: str = None
#     filesize: str = None
#     filetype: str = None
#     floor: str = None
#     floor_xlink: int = None
#     info: str = None


# TODO Netdot REST API seems to not return blob data
# @dataclass
# class ClosetPicture(NetdotAPIDataclass, CSVDataclass):
#     NETDOT_MENU_URL_PATH = "management"
#     NETDOT_TABLE_NAME = "ClosetPicture"

#     bindata: str = None
#     closet: str = None
#     closet_xlink: int = None
#     filename: str = None
#     filesize: str = None
