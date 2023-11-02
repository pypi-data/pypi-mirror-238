from contextlib import AbstractContextManager
import functools
import logging
import threading
from datetime import datetime
import inspect
import os
import textwrap
from concurrent.futures import ThreadPoolExecutor
from getpass import getpass
from typing import Callable, List, Union

import uologging

import netdot.dataclasses
from netdot.actions import ActionTypes
from netdot.dataclasses.base import NetdotAPIDataclass
from netdot.unitofwork import UnitOfWork

from . import client, exceptions, utils, defaults

logger = logging.getLogger(__name__)
trace = uologging.trace(logger)


class Repository(AbstractContextManager):
    """Work with Netdot API using Python objects."""

    _initialized = False
    _existing_connection = None

    def __init__(
        self,
        netdot_url,
        user,
        password,
        dry_run=False,
        print_changes=True,
        threads=defaults.THREADS,
        **kwargs,
    ):
        Repository.prepare_class()
        self.netdot_url = netdot_url
        self.user = user
        self._connection = client.Client(
            netdot_url, user, utils.HiddenString(password), **kwargs
        )
        self._thread_count = threads
        self._dry_run = dry_run
        self._print_dry_run_changes = print_changes
        self.proposed_changes = UnitOfWork()
        self._lock = threading.Lock()

    def __exit__(self):  # pragma: no cover
        self._connection.logout()

    def _create_thread_pool(self):
        return ThreadPoolExecutor(self._thread_count)

    def __str__(self):
        return f"Repository('{self.connection.netdot_url}', '{self.user}')"

    @classmethod
    def generate_markdown_docs(cls, heading=True):
        # TODO Consider refactoring so that there is a method that returns a nested dictionary with all all public methods and public fields. That way, we can easily run a change-detection test -- this is effectively our public API, so it would be nice to have visibility over when it changes (e.g. fail CI/CD unless a certain 'updated_public_api=True' build parameter is provided).
        lines = list()
        if heading:
            lines.append('# Netdot Python API Generated Documentation\n')
            lines.append('<div id="netdot-python-api-generated-documentation"> </div>\n')
            lines.append(
                f'> v{netdot.__version__} documentation generated on {datetime.now().strftime("%b %d, %Y at %I:%M%p %Z")}'
            )
            lines.append('>')
            lines.append('> Netdot Python API contains many generated methods.')
            lines.append(
                '> This documentation is intended to help you understand what is available.'
            )
            lines.append('\n\n')
        lines.append(cls._generate_markdown_for_class(Repository))
        for dataclass in NetdotAPIDataclass.__subclasses__():
            lines.append(cls._generate_markdown_for_class(dataclass))
        return (
            '\n\n' + '\n'.join(filter(None, lines)) + '\n\n'
        )  # Why '\n\n' newline padding? In case this markdown is concatenated with other markdown files.

    @staticmethod
    def _generate_markdown_for_class(
        cls,
        internal_methods_can_skip=[  # These 'internal' methods are not very useful to publicly document
            'to_DTO',
            'from_DTO',
            'with_repository',
            'table_header',
            'as_table_row',
        ],
    ):
        lines = list()
        lines.append(f'## class `netdot.{cls.__name__}`\n')
        if hasattr(cls, '_updatable_fields'):
            fields = [
                field if field.name in cls._updatable_fields() else None
                for field in cls.__dataclass_fields__.values()
            ]
            for field in filter(None, fields):
                line = f'- {field.name} ({field.type.__name__})'
                if field.default is not None:
                    line += f' (Default: {field.default})'
                lines.append(line)
            lines.append('')
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        methods = list(filter(
            lambda method_tuple:
            # Filter 'private' (start with _)
            not method_tuple[0].startswith("_")
            # Filter ALL_CAPS_FIELDS (these are constants)
            and not method_tuple[0].upper() == method_tuple[0]
            # Filter 'internal methods that can be skipped'
            and not method_tuple[0] in internal_methods_can_skip,
            methods,
        ))
        Repository._assert_methods_have_docstrings(methods, cls.__name__)
        for name, method in methods:
            lines.append(f'### {name}\n')
            lines.append(f'> ```{name}{inspect.signature(method)}```')
            lines.append('\n```')
            lines.append(inspect.getdoc(method).strip())
            lines.append('```\n')
        return '\n'.join(filter(None, lines))

    @staticmethod
    def _assert_methods_have_docstrings(methods, class_name):
        result = list(filter(lambda tup: tup[1].__doc__ is None, methods))
        if result:
            raise exceptions.NetdotError(f"{class_name} is missing docstrings for methods: {[method[0] for method in result]}")

    def clear_propose_changes(self):
        """Reset the proposed changes (dry run) for this Netdot Repository."""
        self.proposed_changes = UnitOfWork()

    def disable_propose_changes(self):
        """Disable the 'propose changes' or DRY RUN feature on this Netdot Repository.

        After this, all changes will be applied immediately to Netdot.
        """
        self._dry_run = False

    def enable_propose_changes(self, print_changes=True):
        """Enable the 'propose changes' or DRY RUN feature on this Netdot Repository.

        After this, all changes will be queued, only to be applied when `save_changes` is called.
        """
        self._dry_run = True
        self._print_dry_run_changes = print_changes

    def show_changes(self, terse=True):  # pragma: no cover  (wrapper method)
        """Show a 'dry run' of all changes to be made (but don't actually make the changes).

        > See :func:`netdot.UnitOfWork.show_dry_run` for more details.
        """
        self.proposed_changes.show_dry_run(terse)

    def show_changes_as_tables(self, terse=True):  # pragma: no cover  (wrapper method)
        """Print ASCII table(s) representing all of the changes to be made (grouped into tables based on Netdot Data Types).

        > See :func:`netdot.UnitOfWork.show_changes_as_tables` for more details.
        """
        self.proposed_changes.show_changes_as_tables(terse)

    def save_changes(self, confirm=True):
        """_summary_

        Args:
            confirm (bool, optional): _description_. Defaults to True.

        Raises:
            RuntimeError: _description_
        """
        proposed_deletions = self.proposed_changes.with_action_types(
            [ActionTypes.DELETE]
        )
        if proposed_deletions and confirm:  # pragma: no cover (manually tested on Oct 30, 2023)
            print(proposed_deletions.dry_run())
            if not utils.user_confirmation('Deleting is irreversible. Proceed?'):
                print(
                    'Nothing done. Review changes using `show_changes` Type "yes" to proceed next time (or use confirm=False)'
                )
                return

        if self._lock.acquire(blocking=False):
            try:
                prior_dry_run_state = self._dry_run
                self._dry_run = False
                self.proposed_changes.save_changes(self)
                print('Changes saved!')
            finally:
                self._dry_run = prior_dry_run_state
                self._lock.release()
        else:
            raise RuntimeError('Unable to acquire lock for save_changes()')

    def create_new(self, new_data: NetdotAPIDataclass) -> NetdotAPIDataclass:
        """Create some new object in Netdot.

        > NOTE: Upon creation, the `id` field of new_data will be populated.

        Args:
            new_data (netdot.NetdotAPIDataclass): The new data to use for the new Netdot object.

        Returns:
            netdot.NetdotAPIDataclass: The new object (with `id` populated).

        Raises:
            HTTPError: if the object cannot be created for any reason. As an example, expect a generic HTTP 400 when: 
              * an object breaks 'uniqueness' rules (Ex. 2 Sites named "Test"),
              * an object is missing required fields (Ex. a Person without a `lastname`),
              * an object is improperly formatted (Ex. a Device with a `date_installed` that is not a datetime),
        """
        if self._dry_run:
            self.proposed_changes.create(
                new_data, print_changes=self._print_dry_run_changes
            )
            return new_data.with_repository(self)
        response = self.connection.create_object(
            new_data.NETDOT_TABLE_NAME, new_data.to_DTO()
        )
        return new_data._intake_DTO(response).with_repository(self)

    def update(self, new_data: NetdotAPIDataclass) -> NetdotAPIDataclass:
        """Update an existing object in Netdot.

        Args:
            id (int): The ID of the object to update.
            new_data (netdot.NetdotAPIDataclass): The new data to use when updating the object.

        Returns:
            netdot.NetdotAPIDataclass: The object provided by Netdot in response to this HTTP POST.

        Raises:
            HTTPError: if the object cannot be updated for some reason.
        """
        if self._dry_run:
            getter_function = getattr(
                self, f'get_{new_data._pep8_method_friendly_name()}'
            )
            old_data = getter_function(new_data.id)
            self.proposed_changes.update(
                old_data, new_data, print_changes=self._print_dry_run_changes
            )
            return new_data.with_repository(self)
        return self.update_by_id(new_data.id, new_data).with_repository(self)

    def delete(
        self,
        data: NetdotAPIDataclass,
        confirm=True,
        ignore_404=True,
    ):
        """Delete an existing object from Netdot.

        > ⚠ WARNING: This is irreversible. Use with caution.

        Args:
            data (NetdotAPIDataclass): The object to be deleted.
            confirm (bool): Assume interactive and ask user 'Proceed? ...' before deleting. Default True.
            ignore_404 (bool): Default True. Ignore HTTP 404 errors. (Why? no need to delete an object if it doesn't exist!)

        Raises:
            HTTPError: Could occur for various reasons.
            NetdotDeleteError: If the object cannot be deleted for some other reason.
            TypeError: If data is not a subclass of NetdotAPIDataclass.
        """
        if self._dry_run:
            self.proposed_changes.delete(
                data, print_changes=self._print_dry_run_changes
            ) 
            return
        if confirm:  # pragma: no cover (manually tested on Oct 30, 2023)
            if not utils.user_confirmation('Deleting is irreversible. Proceed?'):
                print(
                    'Nothing done. Type "yes" to proceed next time (or use confirm=False)'
                )
                return

        id = data.id
        try:
            self.connection.delete_object_by_id(data.NETDOT_TABLE_NAME, id)
        except exceptions.HTTPError as e:
            if ignore_404 and hasattr(e.response, 'status_code') and e.response.status_code == 404:
                return
            raise exceptions.NetdotDeleteError(
                f'Unable to delete {data.__class__.__name__} with id {id}',
                status_code=e.response.status_code,
                response=e.response.content,
            )

    def update_by_id(self, id: int, new_data: NetdotAPIDataclass) -> NetdotAPIDataclass:
        """Update an existing object in Netdot.

        Args:
            id (int): The ID of the object to update.
            new_data (netdot.NetdotAPIDataclass): The new data to use when updating the object.

        Returns:
            netdot.NetdotAPIDataclass: The object provided by Netdot in response to this HTTP POST.

        Raises:
            HTTPError: if the object cannot be updated for some reason.
        """
        obj_url_path = f'/{new_data.NETDOT_TABLE_NAME}/{id}'
        response = self.connection.post(obj_url_path, new_data.to_DTO())
        return new_data._intake_DTO(response)

    @classmethod
    def _attach_methods(cls, methods):
        for method in methods:
            setattr(cls, method.__name__, method)

    @classmethod
    def prepare_class(cls):
        if not cls._initialized:
            netdot.initialize()
            dataclasses = netdot.NetdotAPIDataclass.__subclasses__()
            cls._attach_methods(generate_CRUD_for_all_dataclasses(dataclasses))
            cls._initialized = True

    @classmethod
    def connect(
        cls, _input=input, _getpass=getpass, propose_changes=True, **kwargs
    ):  # pragma: no cover
        """Connect to NetDot for interactive use.

        Example:
        This method is interactive, and requires you to provide your credentials
             >> repo = Repository.connect()
            What is the URL of the NetDot server? [https://nsdb.uoregon.edu]: ('enter' to use default)
            NetDot username: netdot_user
            NetDot password: (uses getpass module, to securely collect your password)

        With `repo`, you can now retrieve data and better understand the capabilities of this API.
        As an example, you may retrieve ipblock information about a particular IP address.

             >> repo.get_ipblock_by_address('10.0.0.0')
            [IPBlock(id=5065, address=IPv4Address('10.0.0.0'), description='RFC1918 Addresses', ... omitted for brevity...

        Returns:
            netdot.Repository: A repository. Use `help(netdot.Repository)` to learn more.
        """
        # Offer to return an existing connection that has been established before
        if cls._existing_connection:
            use_existing_connection = _input(
                textwrap.dedent(
                    f"""
                Noticed an existing connection: 
                    {cls._existing_connection}

                Would you like to retrieve it instead of setting up a new connection? 
                Reply 'yes', or 'no' [yes]: """
                )
            )
            if not use_existing_connection.lower().startswith('n'):
                return cls._existing_connection

        connection = cls._connect(_input, _getpass, dry_run=propose_changes, **kwargs)
        cls._existing_connection = connection
        if propose_changes:
            msg = """
                NOTICE: Proposing changes (this is a DRY RUN).


                Call `save_changes` to actually create, update, and delete NetDot data.

                How do I use this feature?
                1. Retrieve data using `get_*` methods (and `load_*` methods on those objects).
                2. Update the objects you retrieved directly in code, then either:
                   a) call `create_or_update`, `add_*`, or `delete` directly the object, or
                   b) call `update`, create_new`, or `delete`  on this repository.
                3. [Optional] Call `show_changes` to review what changes have been proposed.
                4. Call `save_changes` to actually create, update, and delete NetDot data!

                > Call `disable_propose_changes` anytime to disable this feature and directly modify NetDot.
                >
                > Use `connect_now` to skip this feature and directly modify NetDot. (Or `propose_changes=False`).
                """
            print(textwrap.dedent(msg))
        return connection

    connect_now = functools.partialmethod(connect, propose_changes=False)
    connect_now.__doc__ = """\
        Directly connect to NetDot for interactive use.
    """

    @classmethod
    def _connect(cls, _input=input, _getpass=getpass, **kwargs):  # pragma: no cover
        default_netdot_url = 'https://nsdb.uoregon.edu'
        netdot_url = (
            _input(f'What is the URL of the NetDot server? [{default_netdot_url}]: ')
            or default_netdot_url
        )
        user = _input('NetDot username: ')
        password = utils.HiddenString(_getpass('NetDot password: '))
        return cls(netdot_url, user, password, **kwargs)

    @property
    def connection(self) -> 'client.Client':
        if not self._connection:
            raise exceptions.NetdotError(
                'Must establish a connection before using this repository.'
            )
        return self._connection

    def get_ipblock_children(self, id: int, **url_params) -> List['netdot.IPBlock']:
        """Get the children of some parent IPBlock.

        > NOTE: This will make `N+1` HTTP Requests (where N is the number of children IPBlocks).

        Args:
            id (int): The ID of the parent IPBlock.

        Returns:
            List[netdot.IPBlock]: The children IPBlocks

        Raises:
            HTTPError: If no such IPBlocks are found.
        """
        data = self.connection.get_objects_by_filter(
            netdot.IPBlock.NETDOT_TABLE_NAME,
            'parent',
            str(id),
            **url_params,
        )
        return [
            netdot.IPBlock.from_DTO(ipblock).with_repository(self) for ipblock in data
        ]

    def _get_entity_by_address(self, address: str, cls, **url_params):
        return self._get_unique_by_filter(cls, 'address', address, **url_params)

    def _get_unique_by_filter(
        self, cls: NetdotAPIDataclass, search_field: str, search_term: str, **url_params
    ) -> NetdotAPIDataclass:
        """Try to retrieve a SINGLE object from netdot.

        Logs a WARNING to the console if multiple objects from netdot match this search.

        Args:
            cls (NetdotAPIDataclass): The type of object to retrieve.
            search_field (str): Which field of 'cls' should we be filtering by?
            search_term (str): The unique search term.

        Returns:
            NetdotAPIDataclass: The parsed object that matches the provided search_field and search_term.
        """
        data = self.connection.get_objects_by_filter(
            cls.NETDOT_TABLE_NAME, search_field, search_term, **url_params
        )
        matching_entities = [
            cls.from_DTO(entity_data).with_repository(self) for entity_data in data
        ]
        if len(matching_entities) > 1:
            logger.warning(
                f'Found more than one matching address for {search_term} ({cls.__name__}): {matching_entities}'
            )
        elif len(matching_entities) < 1:
            return None
        return matching_entities[0]

    def get_physaddr_by_MACAddress(self, address: str) -> 'netdot.PhysAddr':
        """Get some Physical Address from Netdot Address Space.

        Args:
            address (str): The MAC Address to lookup, e.g. "00:00:00:00:00:00"

        Returns:
            netdot.PhysAddr: The Physical Address object that matched the provided address, or None.
        """
        return self._get_entity_by_address(address, netdot.PhysAddr)

    def find_edge_port(self, mac_address: str) -> 'netdot.Interface':
        """Get the Edge Port (Interface) associated to some MAC Address.

        > NOTE: This will make `N+M` HTTP Requests (where N ).

        The idea is to get all device ports whose latest forwarding tables included this address.
        If we get more than one, select the one whose forwarding table had the least entries.

        Args:
            mac_address (str): A MAC Address to lookup.

        Returns:
            netdot.Interface: The edge port associated to the provided MAC Address.

        Raises:
            HTTPError: If the MAC Address cannot be found, or if any subsequent HTTP requests fail.
        """
        physaddr = self.get_physaddr_by_MACAddress(mac_address)
        entries = self.get_fwtableentries_by_physaddr(physaddr)
        if len(entries) == 1:
            return entries[0].load_interface()
        elif len(entries) == 0:  # pragma: no cover
            # Defensive programming: HTTPError will be raised before this could occur.
            return
        timestamps = [entry.infer_timestamp() for entry in entries]
        most_recent_scan_time = max(timestamps)
        most_recent_entries = list(
            filter(lambda entry: entry.infer_timestamp() == most_recent_scan_time, entries)
        )

        # TODO can we omit the calls to get_fwtableentries_by_interface? Perhaps the "entries" already loaded is sufficient to lookup interface_counts.
        def get_related_fwtableentries(entry: netdot.FWTableEntry):
            interface = entry.load_interface()
            return self.get_fwtableentries_by_interface(
                interface, fwtable=entry.fwtable_xlink
            )

        with self._create_thread_pool() as executor:
            related_fwtableentries = executor.map(
                get_related_fwtableentries, most_recent_entries
            )
            least_fwtableentries = min(related_fwtableentries, key=len)
            most_recent_entry = max(least_fwtableentries, key=id)
            return most_recent_entry.load_interface()

    def get_rr_by_address(self, address: str) -> 'netdot.RR':
        """Get a Resource Record from Netdot Address Space, by IP Address.

        Args:
            address (str): The IP Address to lookup, e.g. "10.0.0.123"

        Returns:
            netdot.RR: The Resource Record that matched the provided address.

        Raises:
            HTTPError: If the Resource Record cannot be found.
        """
        ipblock = self.get_ipblock_by_address(address)
        rraddr = self._get_unique_by_filter(netdot.RRADDR, 'ipblock', ipblock.id)
        return self.get_rr(rraddr.rr_xlink)

    def get_ipblock_by_address(self, address: str) -> 'netdot.IPBlock':
        """Get some IP Block from Netdot Address Space.

        Args:
            address (str): The IP Address to lookup, e.g. "10.0.0.0"

        Returns:
            IPBlock: The IPBlock object that matched the provided address, or None.
        """
        return self._get_entity_by_address(address, netdot.IPBlock)

def generate_CRUD_for_all_dataclasses(dataclasses) -> List:
    """Generate the 'CRUD' operations for this repository for all Netdot dataclasses."""
    CRUD_methods = []
    for dataclass in dataclasses:
        CRUD_methods.extend(generate_getters_for_dataclass(dataclass))
    return CRUD_methods


def generate_getters_for_dataclass(dataclass: NetdotAPIDataclass) -> List:
    methods_for_dataclass = generate_xlink_getters(dataclass) + [
        generate_all_getter(dataclass),
        generate_by_id_getter(dataclass),
    ]
    return methods_for_dataclass


def generate_by_id_getter(dataclass: NetdotAPIDataclass):
    #
    # Generate a custom `get_by_id` method for dataclass
    #
    def get_by_id(self, id: int) -> dataclass:
        data = self.connection.get_object_by_id(dataclass.NETDOT_TABLE_NAME, str(id))
        return dataclass.from_DTO(data).with_repository(self)

    get_by_id.__doc__ = f"""Get info about a {dataclass.__name__} from Netdot.

    Args:
        id (int): The ID of the {dataclass.__name__} to retrieve.

    Returns:
        netdot.{dataclass.__name__}: The {dataclass.__name__} with `id`. (raises ValueError if `id` is not found)

    Raises:
        ValueError: if the {dataclass.__name__} cannot be retrieved for some reason.
        NetdotError: if some internal error happens (in this Python Netdot API wrapper, or on the Netdot Server itself).
        """
    get_by_id.__name__ = f'get_{dataclass._pep8_method_friendly_name()}'
    return get_by_id


def generate_all_getter(dataclass) -> Callable:
    def get_all(self, **url_params) -> List[dataclass]:
        data_list = self.connection.get_all(dataclass.NETDOT_TABLE_NAME, **url_params)
        return [dataclass.from_DTO(data).with_repository(self) for data in data_list]

    get_all.__doc__ = f"""Get info about {dataclass._name_pluralized()} from Netdot.

    > NOTE: This will return ALL {dataclass._name_pluralized()} from Netdot if no kwargs are provided.

    Args:
        **kwargs: URL Parameters - Any keyword args will be used as URL Parameters. Ex. (id=1) will be translated to `?id=1` in the URL.

    Returns:
        List[netdot.{dataclass.__name__}]: {dataclass._name_pluralized()} from Netdot (that match provided URL Parameters).

    Raises:
        HTTPError: For any HTTP errors (including HTTP 404 if no matches are found).
        NetdotError: if some internal error happens (in this Python Netdot API wrapper, or on the Netdot Server itself).
        """
    get_all.__name__ = f'get_{dataclass._name_pluralized().lower()}_where'
    return get_all


def _generate_xlink_by_id_getter(dataclass, xlink, xlink_class):
    def xlink_by_id_getter(
        self, other: Union[int, NetdotAPIDataclass], **url_params
    ):
        if isinstance(other, NetdotAPIDataclass):
            other = other.id
        data_list = self.connection.get_objects_by_filter(
            dataclass.NETDOT_TABLE_NAME,
            xlink.replace('_xlink', ''),
            other,
            **url_params,
        )
        return [dataclass.from_DTO(data).with_repository(self) for data in data_list]

    xlink_by_id_getter.__doc__ = f"""Get the list of {dataclass._name_pluralized()} associated to a particular {xlink_class.__name__}.

    Args:
        other (int,NetdotAPIDataclass): The particular {xlink_class.__name__} or its `id`.

    Returns:
        List[netdot.{dataclass.__name__}]: The list of {dataclass._name_pluralized()} associated to the {xlink_class.__name__}.
        """
    xlink_by_id_getter.__name__ = (
        f"get_{dataclass._name_pluralized().lower()}_by_{xlink.replace('_xlink','')}"
    )

    return xlink_by_id_getter


def generate_xlink_getters(my_cls) -> List:
    """Generate custom `get_A[s]_by_B` methods for dataclass, based on its foreign_key_field_names."""
    xlink_getters = []

    for xlink, other_cls in my_cls._related_classes().items():
        xlink_by_id_getter = _generate_xlink_by_id_getter(my_cls, xlink, other_cls)
        xlink_getters.append(xlink_by_id_getter)

    return xlink_getters
