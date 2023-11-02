import logging
from typing import List
import threading
import shutil
from copy import copy

from tqdm import tqdm
from tabulate import tabulate

import netdot
from netdot import actions, defaults
from netdot import NetdotAPIDataclass
from netdot.csv_util import CSVDataclass

logger = logging.getLogger(__name__)


class UnitOfWork:
    """Prepare some set of changes to be made in Netdot. Submit these changes using save_changes()."""

    _initialized = False

    def __init__(
        self,
    ):
        UnitOfWork.prepare_class()
        self._actions: List[actions.NetdotAction] = list()
        self._completed_actions = list()
        self._responses = list()
        self._action_in_progress: actions.NetdotAction = None
        self._lock = threading.Lock()

    @classmethod
    def prepare_class(cls):
        if not cls._initialized:
            netdot.initialize()
            cls._initialized = True

    @classmethod
    def from_action_list(cls, action_list: List['actions.NetdotAction'], **kwargs):
        new_unit_of_work = cls(**kwargs)
        new_unit_of_work._actions = action_list
        return new_unit_of_work

    def as_list(self):
        return list(self._actions)

    def completed_as_list(self):
        return list(self._completed_actions)

    def __len__(self):
        return len(self._actions)

    def __contains__(self, item):
        return item in self._actions

    def __iter__(self):
        return iter(self._actions)

    def __getitem__(self, index):
        return self._actions[index]

    def create(self, new_data: NetdotAPIDataclass, print_changes=False, one_line=True):
        """Create a new object in Netdot.

        Args:
            new_data (netdot.NetdotAPIDataclass): The new data to use when creating the object in Netdot.
            truncate (int): Truncate the message to this many characters. Defaults to None.

        Raises:
            TypeError: If new_data is not a subclass of NetdotAPIDataclass.
        """
        if not isinstance(new_data, NetdotAPIDataclass):
            raise TypeError(
                f'Expect new_data to be subclass of NetdotAPIDataclass, instead got: {type(new_data)}'
            )
        action = actions.NetdotAction(
            actions.ActionTypes.CREATE,
            id=None,
            new_data=new_data,
            old_data=None,
        )
        if print_changes:  # pragma: no cover
            max_chars = None
            if one_line:
                max_chars = shutil.get_terminal_size().columns
            print(action.generate_log_for_action(truncate=max_chars))
        self._actions.append(action)

    def update(
        self,
        old_data: NetdotAPIDataclass,
        new_data: NetdotAPIDataclass,
        print_changes=False,
        one_line=True,
    ):
        """Update an existing object in Netdot.

        Args:
            new_data (netdot.NetdotAPIDataclass): The new data to use when updating.
            old_data (netdot.NetdotAPIDataclass): The old data that is going to be replaced.

        Raises:
            TypeError: If new_data and old_data are not the same type (or not a subclass of NetdotAPIDataclass).
        """
        if (
            # fmt: off
            not isinstance(old_data, type(new_data)) 
            or not isinstance(new_data, NetdotAPIDataclass)
            # fmt: on
        ):
            raise TypeError(
                f'''Invalid argument, expecting both new_data and old_data to be the same subclass of NetdotAPIDataclass, but got: 
    new_data: {new_data}  
    old_data: {old_data}
    '''
            )
        action = actions.NetdotAction(
            actions.ActionTypes.UPDATE,
            id=old_data.id,
            new_data=new_data,
            old_data=old_data,
        )
        if print_changes:  # pragma: no cover
            max_chars = None
            if one_line:
                max_chars = shutil.get_terminal_size().columns
            print(action.generate_log_for_action(truncate=max_chars))
        self._actions.append(action)

    def delete(self, old_data: NetdotAPIDataclass, print_changes=False, one_line=True):
        """Delete an existing object from Netdot.

        Args:
            old_data (netdot.NetdotAPIDataclass): The object that will be deleted (must include an 'id').

        Raises:
            TypeError: If old_data is not a subclass of NetdotAPIDataclass.
        """
        if not isinstance(old_data, NetdotAPIDataclass):
            raise TypeError(
                f'Expect old_data to be subclass of NetdotAPIDataclass, instead got: {old_data}'
            )
        action = actions.NetdotAction(
            actions.ActionTypes.DELETE,
            id=old_data.id,
            new_data=None,
            old_data=old_data,
        )
        if print_changes:  # pragma: no cover
            max_chars = None
            if one_line:
                max_chars = shutil.get_terminal_size().columns
            print(action.generate_log_for_action(truncate=max_chars))

        self._actions.append(action)

    def without_action_types(self, action_types: List['actions.ActionTypes']):
        """Get a copy of this Unit of Work with the selected actions removed.

        Args:
            action_types (List[actions.NetdotAction]): The types of actions to be removed.

        """

        def is_action_of_interest(action: actions.NetdotAction):
            return action.action_type not in action_types

        filtered_actions_list = list(filter(is_action_of_interest, self._actions))
        return UnitOfWork.from_action_list(filtered_actions_list)

    def with_action_types(self, action_types: List['actions.SiteActionTypes']):
        """Get a copy of this Unit of Work containing ONLY the selected actions.

        Args:
            action_types (List[actions.NetdotAction]): The types of actions to keep.
        """

        def is_action_of_interest(action: actions.NetdotAction):
            return action.action_type in action_types

        filtered_actions_list = list(filter(is_action_of_interest, self._actions))
        return UnitOfWork.from_action_list(filtered_actions_list)

    def with_data_type(self, data_type: NetdotAPIDataclass):
        """Get a copy of this Unit of Work containing actions of ONLY the selected data type.

        Args:
            data_type (NetdotAPIDataclass): The type of data to keep.
        """

        def is_action_of_interest(action: actions.NetdotAction):
            return isinstance(action.new_data, data_type) or isinstance(
                action.old_data, data_type
            )

        filtered_actions_list = list(filter(is_action_of_interest, self._actions))
        return UnitOfWork.from_action_list(filtered_actions_list)

    def failed_action(self) -> actions.NetdotAction:
        return self._action_in_progress

    def failed_action_msg(self) -> str:
        """If 'save_changes' failed on some task, use this to get info about the failed action.

        Returns:
            str: The message for the task
        """
        if self.failed_action():
            log_message = self.failed_action().generate_log_for_action()
            return f'Failed Action: {log_message}'
        return None

    def show_changes_as_tables(self, terse=True):
        """Print ASCII table(s) representing all of the changes to be made (grouped into tables based on Netdot Data Types)."""
        print(self.changes_as_tables(terse=terse))

    def changes_as_tables(self, terse=True) -> str:
        """Return ASCII table(s) representing all of the changes to be made (grouped into tables based on Netdot Data Types)."""
        tabulated_results = []
        for dataclass in sorted(
            NetdotAPIDataclass.__subclasses__(), key=lambda c: c.__name__
        ):
            columns = ['action'] + dataclass.table_header()
            column_width = None
            if terse:
                # ! Does NOT dynamically adjust number of columns based on data, only based on 
                console_width = shutil.get_terminal_size().columns
                column_width = defaults.TERSE_COL_WIDTH
                terse_col_count_max = console_width // column_width
                columns = columns[:terse_col_count_max]
            data_as_table = self._tabulate_changes(dataclass, columns, column_width)
            if data_as_table:
                tabulated_results.append(
                    f'## {dataclass.__name__} Changes' + '\n\n' + data_as_table
                )
        return '\n\n\n'.join(tabulated_results)

    def show_dry_run(self, one_line=True):
        """Show a 'dry run' of all changes to be made (but don't actually make the changes).

        Prints a log message for each action in this UnitOfWork."""
        print(self.dry_run(one_line=one_line))

    def dry_run(self, one_line=True) -> str:
        """Return a 'dry run' of all changes to be made (but don't actually make the changes).

        Returns a log message for each action in this UnitOfWork."""
        indentation = self._calculate_indent()
        max_chars = None
        if one_line:
            terminal_width = shutil.get_terminal_size().columns
            max_chars = terminal_width - indentation - len('. ')
        dry_run_actions = list()
        for count, action in enumerate(self._actions):
            msg = action.generate_log_for_action(max_chars)
            dry_run_actions.append(f'{count+1:{indentation}d}. {msg}')
        return '\n'.join(dry_run_actions)

    def _calculate_indent(self):
        indentation = 1
        count = len(self._actions)
        start = 1
        while start < count:
            start *= 10
            indentation += 1
        return indentation

    def _tabulate_changes(
        self, dataclass: CSVDataclass, selected_columns=None, maxcolwidths=16
    ):
        table_data = self.with_data_type(dataclass)
        if not table_data:
            return

        selected_data_columns = copy(selected_columns)
        selected_data_columns.remove('action')
        rows = [row.as_table_row(selected_data_columns) for row in table_data.as_list()]
        return tabulate(
            rows,
            table_data[0].table_header()[: len(selected_columns)],
            maxcolwidths=maxcolwidths,
        )

    def save_changes(self, netdot_repo: 'netdot.Repository'):
        """Save the changes back to Netdot.

        > Important: If an action cannot be completed for some reason, you might want to
            1. The action that failed is available via :func:`failed_action()`
            2. All completed actions are available via :func:`completed_as_list()`
            3. All remaining (incomplete) actions are available via :func:`as_list()`
            this method may have completed some changes but the remaining changes will be skipped.

        Args:
            netdot_repo (netdot.Repository): The repository to use when saving changes.
        """
        save_functions = {
            actions.ActionTypes.UPDATE: lambda action: netdot_repo.update(
                action.new_data,
            ),
            actions.ActionTypes.CREATE: lambda action: netdot_repo.create_new(
                action.new_data
            ),
            actions.ActionTypes.DELETE: lambda action: netdot_repo.delete(
                action.old_data, confirm=False, ignore_404=False
            ),
        }

        def save_change(action: 'actions.NetdotAction', one_line=True):
            max_chars = None
            if one_line:
                max_chars = shutil.get_terminal_size().columns
            save_function = save_functions[action.action_type]
            logger.info(action.generate_log_for_action(truncate=max_chars))
            result = save_function(action)
            logger.info(
                action.generate_log_for_action(truncate=max_chars, completed=True)
            )
            return result

        if self._lock.acquire(blocking=False):
            try:
                for action in tqdm(list(self._actions)):
                    # Remove action before performing it.
                    # ! Why? Ensure that action will not be performed twice.
                    self._actions.remove(action)
                    self._action_in_progress = action
                    # TODO Want to ensure that any ID that has been populated by Netdot makes it into future actions
                    response = save_change(action)
                    self._action_in_progress = None
                    self._completed_actions.append(action)
                    self._responses.append(response)
            except Exception as e:
                logger.exception(
                    f'Failed to save changes to Netdot. Summary: {len(self._completed_actions)} completed actions, {len(self._actions)+1} remaining actions, including failed action: {self._action_in_progress}'
                )
                raise e
            finally:
                self._lock.release()
        else:
            raise RuntimeError('Unable to acquire lock for save_changes()')
