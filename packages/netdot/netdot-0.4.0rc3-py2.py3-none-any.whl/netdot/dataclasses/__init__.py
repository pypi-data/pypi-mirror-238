from .asset import Asset
from .base import NetdotAPIDataclass
from .bgp import ASN, BGPPeering
from .cables import (
    HorizontalCable,
    BackboneCable,
    CableType,
    CableStrand,
    Circuit,
    CircuitStatus,
    CircuitType,
    FiberType,
    Splice,
    StrandStatus,
)
from .device import (
    Device,
    DeviceAttr,
    DeviceAttrName,
    DeviceContacts,
    DeviceModule,
    OUI,
    STPInstance,
)
from .dhcp import (
    DHCPAttr,
    DHCPAttrName,
    DHCPScope,
    DHCPScopeType,
    DHCPScopeUse,
)
from .dns import (
    Zone,
    ZoneAlias,
    RR,
    RRADDR,
    RRCNAME,
    RRDS,
    RRHINFO,
    RRLOC,
    RRMX,
    RRNAPTR,
    RRNS,
    RRPTR,
    RRSRV,
    RRTXT,
)
from .entity import Entity, EntityRole, EntitySite, EntityType
from .interface import Interface, InterfaceVLAN
from .ipblock import (
    IPBlock,
    IPBlockAttr,
    IPBlockAttrName,
    IPBlockStatus,
    IPService,
    Service,
    SubnetZone,
)
from .products import Product, ProductType
from .site import (
    Closet,
    # ClosetPicture,
    Room,
    Floor,
    # FloorPicture,
    Site,
    SiteLink,
    # SitePicture,
    SiteSubnet,
)
from .vlan import VLAN, VLANGroup
from .physaddr import PhysAddr, PhysAddrAttr, PhysAddrAttrName
from .fwtable import FWTable, FWTableEntry
from .users import (
    Person,
    UserRight,
    UserType,
    Contact,
    ContactList,
    ContactType,
    AccessRight,
    Audit,
    GroupRight,
)
from .misc import (
    Availability,
    # DataCache,
    HostAudit,
    MaintContract,
    MonitorStatus,
    SavedQueries,
    SchemaInfo,
)


_initialized = False


def initialize():
    # TODO can these just be at module-level instead of having this be a runtime function?
    global _initialized
    if not _initialized:
        AccessRight()
        ASN()
        Asset()
        Audit()
        Availability()
        BackboneCable()
        BGPPeering()
        CableStrand()
        CableType()
        Circuit()
        CircuitStatus()
        CircuitType()
        Closet()
        # ClosetPicture()
        Contact()
        ContactList()
        ContactType()
        # DataCache()
        Device()
        DeviceAttr()
        DeviceAttrName()
        DeviceContacts()
        DeviceModule()
        DHCPAttr()
        DHCPAttrName()
        DHCPScope()
        DHCPScopeType()
        DHCPScopeUse()
        Entity()
        EntityRole()
        EntitySite()
        EntityType()
        FiberType()
        Floor()
        # FloorPicture()
        FWTable()
        FWTableEntry()
        GroupRight()
        HorizontalCable()
        HostAudit()
        Interface()
        InterfaceVLAN()
        IPBlock()
        IPBlockAttr()
        IPBlockAttrName()
        IPBlockStatus()
        IPService()
        MaintContract()
        MonitorStatus()
        OUI()
        Person()
        PhysAddr()
        PhysAddrAttr()
        PhysAddrAttrName()
        Product()
        ProductType()
        Room()
        RR()
        RRADDR()
        RRCNAME()
        RRCNAME()
        RRDS()
        RRHINFO()
        RRLOC()
        RRMX()
        RRNAPTR()
        RRNS()
        RRPTR()
        RRSRV()
        RRTXT()
        SavedQueries()
        SchemaInfo()
        Service()
        Site()
        SiteLink()
        # SitePicture()
        SiteSubnet()
        Splice()
        STPInstance()
        StrandStatus()
        SubnetZone()
        UserRight()
        UserType()
        VLAN()
        VLANGroup()
        Zone()
        ZoneAlias()
        _initialized = True


Subnet = IPBlock
IPAddr = IPBlock
IPContainer = IPBlock

__all__ = [
    "initialize",
    "NetdotAPIDataclass",
    "AccessRight",
    "ASN",
    "Asset",
    "Audit",
    "Availability",
    "BackboneCable",
    "BGPPeering",
    "CableStrand",
    "CableType",
    "Circuit",
    "CircuitStatus",
    "CircuitType",
    "Closet",
    # "ClosetPicture",
    "Contact",
    "ContactList",
    "ContactType",
    "DataCache",
    "Device",
    "DeviceAttr",
    "DeviceAttrName",
    "DeviceContacts",
    "DeviceModule",
    "DHCPAttr",
    "DHCPAttrName",
    "DHCPScope",
    "DHCPScopeType",
    "DHCPScopeUse",
    "Entity",
    "EntityRole",
    "EntitySite",
    "EntityType",
    "FiberType",
    "Floor",
    # "FloorPicture",
    "FWTable",
    "FWTableEntry",
    "GroupRight",
    "HorizontalCable",
    "HostAudit",
    "Interface",
    "InterfaceVLAN",
    "IPBlock",
    "IPBlockAttr",
    "IPBlockAttrName",
    "IPBlockStatus",
    "IPService",
    "MaintContract",
    "MonitorStatus",
    "OUI",
    "Person",
    "PhysAddr",
    "PhysAddrAttr",
    "PhysAddrAttrName",
    "Product",
    "ProductType",
    "Room",
    "RR",
    "RRADDR",
    "RRCNAME",
    "RRCNAME",
    "RRDS",
    "RRHINFO",
    "RRLOC",
    "RRMX",
    "RRNAPTR",
    "RRNS",
    "RRPTR",
    "RRSRV",
    "RRTXT",
    "SavedQueries",
    "SchemaInfo",
    "Service",
    "Site",
    "SiteLink",
    # "SitePicture",
    "SiteSubnet",
    "Splice",
    "STPInstance",
    "StrandStatus",
    "SubnetZone",
    "UserRight",
    "UserType",
    "VLAN",
    "VLANGroup",
    "Zone",
    "ZoneAlias",
]
