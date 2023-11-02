from typing import Callable, ClassVar, Dict, List, Set
import dataclasses
import ipaddress
import logging
import textwrap
from typing import Tuple

import netdot
import netdot.exceptions
from netdot.csv_util import CSVDataclass
from netdot import parse, utils, defaults

logger = logging.getLogger(__name__)


inconsistent_and_ignorable_fields = set(
    [
        'info',
        'ttl',
    ]
)


def handle_None_values(dto):
    # ! TODO Do we ever need to send an empty string when None is provided??
    return {k: v for k, v in dto.items() if bool(v) is True}


def handle_bool_values(dto):
    return {k: str(int(v)) if isinstance(v, bool) else v for k, v in dto.items()}


def handle_xlink_fields(dto):
    # Convert _xlink fields to remove the suffix, and send ID only
    return {k.replace('_xlink', ''): v for k, v in dto.items()}


@dataclasses.dataclass
class NetdotAPIDataclass(CSVDataclass):
    #
    # Class variables
    #
    _initialized: ClassVar[bool] = False
    _logged_unused_fields: ClassVar[Set] = None
    _xlink_class_map: ClassVar[Dict[str, str]] = dict()
    _associative_table: ClassVar[bool] = False
    NETDOT_TABLE_NAME: ClassVar[str]
    NETDOT_MENU_URL_PATH: ClassVar[str]  # Useful for generating web_url
    DEFAULT_DTO_FIELD_PARSERS: ClassVar = {
        "*_xlink": parse.ID_from_xlink,
    }

    #
    # Default dataclass fields
    #
    id: int = None
    # pylint: disable-next=undefined-variable
    _repository: "netdot.Repository" = dataclasses.field(  # noqa
        default=None, repr=False
    )

    @classmethod
    def table_header(cls) -> Tuple[str, ...]:
        return ['id'] + cls._updatable_fields()

    def as_table_row(self, select_columns=None) -> Tuple[str, ...]:
        columns = select_columns or self.table_header()
        return super().as_table_row(columns)

    @classmethod
    def _associative_table_other_class(cls, other_cls: "NetdotAPIDataclass"):
        """Get the class that is different from 'other_cls'."""
        if not cls._associative_table:
            raise TypeError(
                'This method is only valid for associative tables (many to many relationship only).'
            )
        cls_options = list(cls._related_classes().values())
        cls_options.remove(other_cls)
        return cls_options[0]

    @classmethod
    def _associative_table_other_class_xlink_name(cls, other_cls: "NetdotAPIDataclass"):
        inv_xlink_class_map = {v: k for k, v in cls._xlink_class_map.items()}
        return (
            inv_xlink_class_map[other_cls.__name__]
            if other_cls.__name__ in inv_xlink_class_map
            else other_cls.__name__.lower()
        )

    def __setattr__(self, name, value):
        """Override setattr to also set the associated '_xlink' field if a NetdotAPIDataclass is provided."""
        if isinstance(value, NetdotAPIDataclass) and hasattr(self, f'{name}_xlink'):
            super().__setattr__(f'{name}_xlink', value.id)
            super().__setattr__(name, value)
            return
        elif name.endswith('_xlink'):
            non_xlink_value = getattr(self, name.replace('_xlink', ''))
            if isinstance(non_xlink_value, NetdotAPIDataclass):
                return
        super().__setattr__(name, value)

    @classmethod
    def prepare_class(cls):
        if not cls._initialized:
            cls._generate_and_attach_others_getAll_methods()
            cls._generate_and_attach_my_getter_methods()
            cls._generate_and_attach_others_m2m_add_methods()
            cls._generate_and_attach_others_add_xlink_methods()
            cls._logged_unused_fields = set()
            cls._initialized = True

    def __post_init__(self):
        self.prepare_class()

    def create(self):
        """Create this object in Netdot. (wrapper around :func:`create_or_update()`)

        Raises:
            ValueError: If trying to create an object that already has an `id`.
        """
        if self.id is not None:
            raise ValueError(
                f"Cannot create an object that already has an `id` (id={self.id}). ID is assigned by database."
            )
        self.create_or_update()

    def update(self):
        """Update this object in Netdot.

        Raises:
            ValueError: If trying to update an object that has no `id`.
        """
        if self.id is None:
            raise ValueError("`id` is required to update an object. None provided.")
        self.create_or_update()

    def create_or_update(self: "NetdotAPIDataclass"):
        """Create or update this object in Netdot.

        > NOTE: Upon creation, this object's `id` will be populated.

        Raises:
            HTTPError: if the object cannot be created for any reason. As an example, expect a generic HTTP 400 when: 
              * an object breaks 'uniqueness' rules (Ex. 2 Sites named "Test"),
              * an object is missing required fields (Ex. a Person without a `lastname`),
              * an object is improperly formatted (Ex. a Device with a `date_installed` that is not a datetime),
        """
        self._assert_repository_attached()
        if self.id:  # UPDATE
            create_or_update_function = getattr(self.repository, 'update')
        else:  # CREATE
            create_or_update_function = getattr(self.repository, 'create_new')
        create_or_update_function(self)

    def _intake_DTO(self, data: Dict):
        return self._update_my_fields(self.from_DTO(data))

    def _update_my_fields(self, response: 'NetdotAPIDataclass'):
        if not isinstance(response, type(self)):
            raise TypeError(
                f"Expected response to be of type {type(self)}, got {type(response)}"
            )
        fields_to_update = (
            self._updatable_fields()
            + ['id']
            + self.foreign_key_field_names(remove_suffix=True)
        )
        for field_name in fields_to_update:
            setattr(self, field_name, getattr(response, field_name))
        return self

    def _assert_repository_attached(self):
        if not self._repository:
            raise netdot.exceptions.NetdotError(
                'Must have repository attached to use methods like: create, add_*,load_*, update, delete. Use with_repository(...) to fix.'
            )

    def delete(self, **kwargs):
        """Delete this object.

        Args:
            See :func:`netdot.Repository.delete`

        Requires:
            Must have repository attached. Use with_repository(...)
        """
        self._assert_repository_attached()
        self.repository.delete(self, **kwargs)

    @classmethod
    def _attach_methods(cls, methods):
        for method in methods:
            setattr(cls, method.__name__, method)

    @classmethod
    def _pep8_method_friendly_name(cls):
        return cls.__name__.lower()

    @classmethod
    def _name_pluralized(cls):
        return utils.pluralize(cls.__name__)

    @classmethod
    def _get_xlink_class_name(cls, xlink: str):
        try:
            xlink_classname = xlink[: -len("_xlink")]
            return cls._xlink_class_map[xlink_classname]
        except KeyError:
            return xlink

    @classmethod
    def foreign_key_field_names(cls, remove_suffix=False) -> List:
        """TODO

        Returns:
            List:

        Examples:

        >>> import netdot
        >>> netdot.BackboneCable.foreign_key_field_names()
        ['end_closet_xlink', 'owner_xlink', 'start_closet_xlink', 'type_xlink']

        >>> netdot.Site.foreign_key_field_names()
        ['availability_xlink', 'contactlist_xlink']

        """
        # Get all keys ending with the _xlink suffix. Example: asset_id_xlink
        #
        new_keys = cls.__dataclass_fields__.keys()
        foreign_keys = list(
            filter(
                lambda field_name: field_name.endswith("_xlink"),
                new_keys,
            )
        )
        if remove_suffix:
            return [key.replace('_xlink', '') for key in foreign_keys]
        return foreign_keys

    @classmethod
    def _related_classes(cls) -> Dict[str, "NetdotAPIDataclass"]:
        """Provide a dictionary holding all of the 'xlink' field names and their associated dataclasses.

        Returns:
            Dict[str, "NetdotAPIDataclass"]: All the associated fields, and their data classes.

        Example:

            >>> import netdot
            >>> netdot.BackboneCable._related_classes()
            {'end_closet_xlink': <class '...Closet'>, 'owner_xlink': <class '...Entity'>, 'start_closet_xlink': <class '...Closet'>, 'type_xlink': <class '...CableType'>}

            >>> netdot.Site._related_classes()
            {'availability_xlink': <class 'netdot...Availability'>, 'contactlist_xlink': <class 'netdot...ContactList'>}

        """
        related_object_types = {}
        for xlink in cls.foreign_key_field_names():
            xlink_class_name = cls._get_xlink_class_name(xlink)
            xlink_class_name = xlink_class_name.replace("_xlink", "")
            for other_dataclass in NetdotAPIDataclass.__subclasses__():
                if xlink_class_name.lower() == other_dataclass.__name__.lower():
                    related_object_types[xlink] = other_dataclass

        return related_object_types

    @classmethod
    def _updatable_fields(cls) -> List[str]:
        """Fields that can be updated via the Netdot API.

        Returns:
            List[str]: Names of the fields of this object that can be updated.

        Example:

            >>> import netdot
            >>> netdot.Site._updatable_fields()
            ['name', 'aliases', 'availability_xlink', 'contactlist_xlink', 'gsf', 'number', 'street1', 'street2', 'state', 'city', 'country', 'zip', 'pobox', 'info']

        """
        return list(
            filter(
                lambda field_name:
                # Filter 'private' (start with _)
                not field_name.startswith("_")
                # Filter ALL_CAPS_FIELDS (these are constants)
                and not field_name.upper() == field_name
                # Filter 'id' (should only be provided via URL path)
                and not field_name == "id"
                # Filter the 'shallow-copy' fields (we only want '_xlink' fields)
                # All _xlink fields are foreign keys, they should be updated
                # However, there is also a shallow field associated to each _xlink field.
                # The shallow 'str' fields should NOT be sent in DTO.
                and field_name not in cls.foreign_key_field_names(remove_suffix=True),
                cls.__dataclass_fields__.keys(),
            )
        )

    def to_DTO(self) -> Dict:
        """Convert to a Data Transfer Object (compliant with NetDot REST API).

        Returns:
            Dict: Use as input to Netdot API POST calls, for creation/update operations.

        Example:

            >>> import netdot
            >>> contact_list = netdot.ContactList(id=123, name='foo')
            >>> site = netdot.Site(name='foo', contactlist=contact_list, city='Eugene')
            >>> site.to_DTO()
            {'name': 'foo', 'contactlist': 123, 'city': 'Eugene'}

        """
        # Create a dict (DTO) that represents this object
        dto = dict()
        self._update_my_fields(self)
        for field in self._updatable_fields():
            # if field.endswith('_xlink'):
            #     xlink_field = field.replace('_xlink', '')
            #     xlink_object = getattr(self, xlink_field)
            #     if isinstance(xlink_object, NetdotAPIDataclass):
            #         dto[field] = xlink_object.id
            #         continue
            dto[field] = getattr(self, field)
        return handle_bool_values(handle_None_values(handle_xlink_fields(dto)))

    # def _intake_xlink_field(self, field):
    #     if not field.endswith('_xlink'):  # pragma: no cover
    #         raise TypeError("This method is only valid for _xlink fields.")
    #     xlink_field = field.replace('_xlink', '')
    #     xlink_object = getattr(self, xlink_field)
    #     if isinstance(xlink_object, NetdotAPIDataclass):
    #         return xlink_object.id
    #     else:
    #         return getattr(self, field)

    @classmethod
    def is_xlink_sibling(cls, field_name):
        return f'{field_name}_xlink' in vars(cls).keys()

    @classmethod
    def _parse_DTO_field(cls, field_name: str, data: dict, string_parser):
        dto_field_name = field_name.rstrip('_')
        field_value = str(data[dto_field_name])
        if not isinstance(string_parser, str) and field_value.strip() == '':
            return field_value  # Don't try to parse empty strings into ints, bools, etc
        if string_parser == ipaddress.ip_address and field_value == '0':
            return None  # Don't try to parse '0' into an IP Address
        parsed_value = string_parser(data[dto_field_name])
        if cls.is_xlink_sibling(field_name) and parsed_value == "0":
            # If it is a sibling of xlink field, then filter "0" response to instead be "None"
            return None
        else:
            return parsed_value

    @classmethod
    def from_DTO(
        cls,
        DTO_data: Dict,
        DTO_field_parsers: Dict = DEFAULT_DTO_FIELD_PARSERS,
        raise_parse_errors=defaults.RAISE_PARSE_ERRORS,
        warn_missing_fields=defaults.WARN_MISSING_FIELDS,
    ) -> "NetdotAPIDataclass":
        """Parse data retrieved from Netdot API into a NetdotAPIDataclass.

        Args:
            data_transfer_object (Dict): Dictionary of raw data returned from Netdot API.
            dto_field_parsers (Dict, optional): A dictionary holding field_name -> parse_field() functions.
                This is useful for when data returned from the NetDot API is not a string but actually some other data type.
                Defaults to DEFAULT_STRING_PARSERS. By default, all fields are parsed as strings.
                field_name may contain a single wildcard at the beginning, e.g. *_xlink will expand to used_by_xlink, owner_xlink, parent_xlink, etc...
            continue_on_parse_error (bool, optional): If True, will continue parsing even if a field cannot be parsed.

        Returns:
            NetdotAPIDataclass: The appropriate subclass of NetdotAPIDataclass.
        """
        if not DTO_data:
            raise ValueError(
                f"Cannot parse empty Data Transfer Object (DTO): {DTO_data}."
            )
        data = dict(DTO_data.copy())
        missing_fields = []
        if DTO_field_parsers:
            field_parsers = dict(DTO_field_parsers.copy())
            field_parsers.update(cls.infer_base_parsers())
            field_parsers.update(cls.expand_wildcard_parsers(field_parsers))
            for field_name, string_parser in field_parsers.items():
                if field_name.startswith("_") or field_name.upper() == field_name:
                    continue  # Skip '_private' and 'ALL_CAPS' fields
                try:
                    data[field_name] = cls._parse_DTO_field(
                        field_name, data, string_parser
                    )
                    if field_name.endswith("_"):
                        del data[field_name.rstrip('_')]
                except KeyError:
                    if field_name.endswith("_xlink"):
                        continue  # Expect _xlink to be absent if it is unset in Netdot
                    missing_fields.append(field_name)
                except Exception as parse_error:
                    logger.warning(
                        textwrap.dedent(
                            f"""\
                            Unable to parse '{field_name}' for '{cls.__name__}', value: {data[field_name]}
                            (Using parser {str(string_parser)}, got error: {parse_error})"""
                        )
                    )
                    if raise_parse_errors:
                        raise parse_error
        if warn_missing_fields and set(missing_fields).difference(
            inconsistent_and_ignorable_fields
        ):
            logger.warning(
                f"NetDot '{cls.__name__}' response missing field(s): {missing_fields}"
            )
        return cls._parse_data_transfer_obj(data)

    @classmethod
    def _parse_data_transfer_obj(cls, data_transfer_object):
        """Parse some data retrieved from Netdot into a proper NetdotAPIDataclass.

        Args:
            data_transfer_object (Dict): Dictionary of raw data returned from Netdot API.

        Returns:
            NetdotAPIDataclass: The appropriate subclass of NetdotAPIDataclass.
        """
        cls._log_unknown_fields(data_transfer_object)

        # Construct the new object!
        fields_to_parse = cls._get_known_fields(data_transfer_object)
        data_to_parse = {key: data_transfer_object[key] for key in fields_to_parse}
        return cls(**data_to_parse)

    @classmethod
    def _get_known_fields(cls, data_transfer_object):
        valid_fields = set(
            [field_name.rstrip('_') for field_name in cls.__dataclass_fields__.keys()]
        )
        valid_fields |= set(cls.__dataclass_fields__.keys())
        provided_fields = set(data_transfer_object.keys())
        return provided_fields.intersection(valid_fields)

    @classmethod
    def _get_unknown_fields(cls, data_transfer_object):
        valid_fields = set(
            [field_name.rstrip('_') for field_name in cls.__dataclass_fields__.keys()]
        )
        valid_fields |= set(cls.__dataclass_fields__.keys())
        provided_fields = set(data_transfer_object.keys())
        return provided_fields.difference(valid_fields)

    @classmethod
    def _log_unknown_fields(cls, data_transfer_object):
        unused_fields = cls._get_unknown_fields(data_transfer_object)
        if unused_fields:
            unused_data = {key: data_transfer_object[key] for key in unused_fields}
            # Always log a debug message with ALL the data
            logger.debug(
                f"Unparsed data ({cls.__module__}.{cls.__name__}): {unused_data}"
            )
            # If this is the first time we've seen these 'unused field(s)', then log a warning!
            if not unused_fields.issubset(cls._logged_unused_fields):
                cls._logged_unused_fields = cls._logged_unused_fields.union(
                    unused_fields
                )
                logger.warning(
                    f"Received unknown field(s): {unused_data} "
                    + f"(to fix, add unknown field(s) to {cls.__module__}.{cls.__name__} )"
                )

    @classmethod
    def expand_wildcard_parsers(cls, DTO_field_parsers: Dict[str, Callable]) -> None:
        """Expand any 'wildcard' parsers.
        NOTICE: This method updates the provided Dict in place.

        If any of DTO_field_parsers starts with "*", they will be expanded to match any of the fields available in DTO_data.

        Example:

            Assume we have NetdotAPIDataclass FooAddress.

            >> from dataclasses import dataclass
            >> @dataclass
            .. class FooAddress(NetdotAPIDataclass):
            ..     local_addr: ipaddress.ip_address
            ..     mgmt_addr: ipaddress.ip_address

            >> DTO_field_parsers = { '*_addr': ipaddress.ip_address }

            >> FooAddress.expand_wildcard_parsers(DTO_field_parsers)
            {'local_addr': <function ip_address ...>, 'mgmt_addr': <function ip_address ...>}
        """

        def is_wildcard_pattern(field_name):
            return field_name.startswith("*") or field_name.endswith("*")

        wildcard_patterns = filter(is_wildcard_pattern, DTO_field_parsers)
        wildcard_parsers = {
            pattern: DTO_field_parsers[pattern] for pattern in wildcard_patterns
        }
        for wildcard_pattern, parser in wildcard_parsers.items():
            del DTO_field_parsers[wildcard_pattern]
            pattern = wildcard_pattern.strip("*")
            for actual_field_name in cls.__dataclass_fields__:
                if (
                    wildcard_pattern.startswith("*")
                    and actual_field_name.endswith(pattern)
                ) or (
                    wildcard_pattern.endswith("*")
                    and actual_field_name.startswith(pattern)
                ):
                    DTO_field_parsers[actual_field_name] = parser
        return DTO_field_parsers

    @classmethod
    def infer_base_parsers(cls) -> Dict[str, Callable]:
        base_parsers = {
            field_name: dataclass_field.type
            for field_name, dataclass_field in cls.__dataclass_fields__.items()
            # if dataclass_field.type is not str
        }
        for field_name, parser in base_parsers.items():
            if parser is bool:
                base_parsers[field_name] = parse.Boolean
        return base_parsers

    @property
    def web_url(self) -> str:
        submenu_web_url = {
            "cable_plant": self._web_url2,
            "management": self._web_url1,
            "generic": self._web_url2,
        }
        web_url_function = submenu_web_url[self.NETDOT_MENU_URL_PATH]
        return web_url_function()

    def _web_url1(self) -> str:
        if hasattr(self, "NETDOT_URL_PATH"):
            url_path = (
                f"/{self.NETDOT_MENU_URL_PATH}/{self.NETDOT_URL_PATH.lower()}.html"
            )
        else:
            url_path = (
                f"/{self.NETDOT_MENU_URL_PATH}/{self.NETDOT_TABLE_NAME.lower()}.html"
            )
        return f"{self.netdot_url}{url_path}?id={self.id}"

    def _web_url2(self) -> str:
        url_path = f"/{self.NETDOT_MENU_URL_PATH}/view.html"
        params = f"table={self.NETDOT_TABLE_NAME}&id={self.id}"
        return f"{self.netdot_url}{url_path}?{params}"

    @property
    def netdot_url(self):
        return self.repository.connection.netdot_url

    @property
    def repository(self) -> "netdot.Repository":
        return self._repository

    def with_repository(self, repository: "netdot.Repository") -> "NetdotAPIDataclass":
        """Add your Netdot repository to this object (to simplify `create_or_update`, `load_*`, etc)."""
        self._repository = repository
        return self

    @classmethod
    def _generate_and_attach_others_m2m_add_methods(cls):
        for xlink, xlink_dataclass in cls._related_classes().items():
            if cls._associative_table:
                xlink_adder = cls._generate_your_many_to_many_add_method(
                    xlink, xlink_dataclass
                )
                xlink_dataclass._attach_methods([xlink_adder])

    @classmethod
    def _generate_and_attach_others_add_xlink_methods(cls):
        for xlink, xlink_dataclass in cls._related_classes().items():
            xlink_adder = cls._generate_your_xlink_add_method(
                xlink,
                xlink_dataclass,
                include_xlink_in_name=cls._related_class_repeats(xlink_dataclass),
            )
            xlink_dataclass._attach_methods([xlink_adder])

    @classmethod
    def _generate_and_attach_my_getter_methods(cls):
        for xlink, xlink_dataclass in cls._related_classes().items():
            xlink_loader = cls._generate_my_xlink_load_method(xlink, xlink_dataclass)
            cls._attach_methods([xlink_loader])

    @classmethod
    def _related_class_repeats(cls, other_cls: "NetdotAPIDataclass"):
        return list(cls._related_classes().values()).count(other_cls) > 1

    @classmethod
    def _generate_and_attach_others_getAll_methods(cls):
        """Generate all the 'load_XXXs' methods for classes that this class is referenced by."""
        for xlink, dataclass in cls._related_classes().items():
            xlink_loaders = list()
            if cls._associative_table:
                xlink_loaders.append(
                    cls._generate_your_many_to_many_load_method(xlink, dataclass)
                )
                xlink_loaders.append(
                    cls._generate_your_xlink_load_method(xlink, dataclass)
                )
            else:
                xlink_loaders.append(
                    cls._generate_your_xlink_load_method(
                        xlink,
                        dataclass,
                        include_xlink_in_name=cls._related_class_repeats(dataclass),
                    )
                )
            dataclass._attach_methods(xlink_loaders)

    @classmethod
    def _generate_my_xlink_load_method(my_cls, xlink, other_cls):
        """Generate the `load_xlink()` method to be attached to cls.

        E.g. will generate load_site() when other_cls is netdot.Site.
        """

        def xlink_loader(self) -> other_cls:  # type: ignore
            self._assert_repository_attached()
            xlink_id = getattr(self, xlink)
            if not xlink_id:
                # TODO: Should we raise an exception here?? (In general, we expect HTTPError whenever we 'fail to load an object'...)
                return None
            download_function_name = f"get_{other_cls._pep8_method_friendly_name()}"
            download_function = getattr(self.repository, download_function_name)
            return download_function(xlink_id)

        xlink_loader.__doc__ = f"""Load the {other_cls.__name__} associated to this {my_cls.__name__}.

    Returns:
        netdot.{other_cls.__name__}: The full {other_cls.__name__} object that is related to this {my_cls.__name__}.
            """
        xlink_loader.__name__ = f"load_{xlink.replace('_xlink', '')}"
        return xlink_loader

    @classmethod
    def _generate_your_many_to_many_add_method(
        cls, xlink: str, my_cls: "NetdotAPIDataclass"
    ):
        """Generate a `add_xlinks()` method to be attached to my_cls (NOT m2m_cls)

        E.g. will generate add_device() when my_cls is netdot.Device
        """
        m2m_cls = cls
        other_cls = m2m_cls._associative_table_other_class(my_cls)
        other_cls_xlink_name = m2m_cls._associative_table_other_class_xlink_name(
            other_cls
        )

        def xlink_adder(self, data: other_cls) -> other_cls:
            self._assert_repository_attached()
            new_object = m2m_cls(
                **{
                    other_cls_xlink_name: data,
                    my_cls._pep8_method_friendly_name(): self,
                }
            )
            return self.repository.create_new(new_object)

        xlink_adder.__doc__ = f"""Add a {other_cls.__name__} to this {my_cls.__name__} (via {m2m_cls.__name__}).

        Args:
            data (netdot.{other_cls.__name__}): The {other_cls.__name__} to add to this {my_cls.__name__}.

        Returns:
            netdot.{m2m_cls.__name__}: The newly created {m2m_cls.__name__}.
        """
        xlink_adder.__name__ = f'add_{other_cls_xlink_name}'
        return xlink_adder

    @classmethod
    def _generate_your_many_to_many_load_method(
        cls, xlink: str, my_cls: "NetdotAPIDataclass"
    ):
        """Generate a `load_xlinks()` method to be attached to my_cls (NOT m2m_cls)

        E.g. will generate load_devices() when my_cls is netdot.Device.
        """
        m2m_cls = cls
        other_cls = m2m_cls._associative_table_other_class(my_cls)
        other_cls_xlink_name = m2m_cls._associative_table_other_class_xlink_name(
            other_cls
        )

        def xlink_loader(self) -> List[other_cls]:
            self._assert_repository_attached()
            # Download all the many-to-many objects
            download_m2m_function_name = f"get_{m2m_cls._name_pluralized().lower()}_by_{xlink.replace('_xlink','')}"
            download_m2m_function = getattr(self.repository, download_m2m_function_name)
            downloaded_m2m_data = download_m2m_function(self.id)
            # Download the data itself
            download_function_name = f"get_{other_cls._pep8_method_friendly_name()}"
            download_function = getattr(self.repository, download_function_name)
            downloaded_data = list()
            for m2m_data in downloaded_m2m_data:
                m2m_other_id = getattr(m2m_data, f'{other_cls_xlink_name}_xlink')
                downloaded_data.append(download_function(m2m_other_id))
            return downloaded_data

        xlink_loader.__doc__ = f"""Load the {utils.pluralize(other_cls_xlink_name)} ({other_cls._name_pluralized()}) associated to this {my_cls.__name__}.

    > NOTE: This will make `N+1` HTTP Requests (where N is the number of {other_cls._name_pluralized()} associated to this {my_cls.__name__}).

    You might prefer :func:`load_{m2m_cls._name_pluralized().lower()}` over this method, if you want to load the many-to-many objects themselves. (and not make N+1 HTTP Requests)

    Returns:
        List[netdot.{other_cls.__name__}]: All {other_cls._name_pluralized()} related to this {my_cls.__name__}.
        """
        xlink_loader.__name__ = f'load_{utils.pluralize(other_cls_xlink_name)}'
        return xlink_loader

    @classmethod
    def _generate_your_xlink_load_method(
        my_cls, xlink: str, other_cls: "NetdotAPIDataclass", include_xlink_in_name=False
    ):
        """Generate the `load_xlinks()` method to be attached to other_cls.

        E.g. will generate load_devices() when my_cls is netdot.Device.
        """

        def xlink_loader(self) -> List[my_cls]:
            self._assert_repository_attached()
            download_function_name = f"get_{my_cls._name_pluralized().lower()}_by_{xlink.replace('_xlink','')}"
            download_function = getattr(self.repository, download_function_name)
            return download_function(self.id)

        xlink_loader.__doc__ = f"""Load the {my_cls._name_pluralized()} associated to this {other_cls.__name__}.

    Returns:
        List[netdot.{my_cls.__name__}]: All {my_cls._name_pluralized()} related to this {other_cls.__name__}.
        """
        method_name = 'load'
        if include_xlink_in_name:
            method_name += f"_{xlink.replace('_xlink','')}"
        method_name += f"_{my_cls._name_pluralized().lower()}"
        xlink_loader.__name__ = method_name
        return xlink_loader

    @classmethod
    def _generate_your_xlink_add_method(
        my_cls, xlink: str, other_cls: "NetdotAPIDataclass", include_xlink_in_name=False
    ):
        """Generate the `add_xlink()` method to be attached to other_cls.

        E.g. will generate add_device() when my_cls is netdot.Device.
        """

        def xlink_adder(self, data: my_cls) -> my_cls:
            self._assert_repository_attached()
            setattr(data, xlink.replace('_xlink', ''), self)
            return self.repository.create_new(data)

        xlink_adder.__doc__ = f"""Add a {my_cls.__name__} to this {other_cls.__name__}.

    Returns:
        netdot.{my_cls.__name__}: The created {my_cls.__name__}.
        """
        method_name = 'add'
        method_name += f"_{my_cls.__name__.lower()}"
        if include_xlink_in_name:
            method_name += f"_as_{xlink.replace('_xlink','')}"

        xlink_adder.__name__ = method_name
        return xlink_adder
