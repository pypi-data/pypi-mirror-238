import datetime
from ipaddress import IPv4Address
import pytest
import logging

from assertpy import assert_that

from netdot import Repository
import netdot
from netdot.actions import ActionTypes, NetdotAction
from netdot.dataclasses.device import Device
from netdot.dataclasses.site import Site


@pytest.mark.vcr
def test_show_changes(repository: Repository, capfd):
    # Arrange
    repository.enable_propose_changes(print_changes=False)
    repository.create_new(netdot.Audit())
    repository.create_new(netdot.Availability())
    repository.create_new(netdot.HorizontalCable())
    repository.create_new(netdot.Device())
    repository.delete(netdot.BGPPeering())
    repository.create_new(netdot.BGPPeering())
    site = repository.get_site(779)
    site.name = 'UPDATED'
    site.create_or_update()

    # Act
    repository.show_changes(terse=True)

    # Assert
    console_output = capfd.readouterr().out
    assert_that(console_output).contains(' 1. Will CREATE Audit: Audit(id=None, fields=None, label=None, object_id=None...')
    assert_that(console_output).contains('2. Will CREATE Availability')
    assert_that(console_output).contains('3. Will CREATE HorizontalCable')
    assert_that(console_output).contains('4. Will CREATE Device')
    assert_that(console_output).contains('5. Will DELETE BGPPeering')
    assert_that(console_output).contains('6. Will CREATE BGPPeering')
    assert_that(console_output).contains('7. Will UPDATE Site')


@pytest.mark.vcr
def test_show_changes_as_tables(repository: Repository, capfd):
    # Arrange
    repository.enable_propose_changes(print_changes=False)
    repository.create_new(netdot.Audit())
    repository.create_new(netdot.Availability())
    repository.create_new(netdot.HorizontalCable())
    repository.create_new(netdot.Device(collect_arp=False))
    repository.delete(netdot.BGPPeering())
    repository.create_new(netdot.BGPPeering())
    site = repository.get_site(137)
    site.name = 'UPDATED'
    site.create_or_update()

    # Act
    repository.show_changes_as_tables(terse=True)

    # Assert
    console_output = capfd.readouterr().out
    assert_that(console_output).contains('''## Audit Changes

action    id    fields    label    object_id    operation
--------  ----  --------  -------  -----------  -----------
CREATE    None  None      None     None         None
''')
    assert_that(console_output).contains('''## Site Changes

action      id  name              aliases    availability_xlink      contactlist_xlink
--------  ----  ----------------  ---------  --------------------  -------------------
UPDATE     137  [-Computing                  None                                  144
                Center
                (039)-]+UPDATED+''')

    

@pytest.mark.vcr
def test_save_changes(repository: Repository, caplog):
    # Arrange
    repository.enable_propose_changes(print_changes=False)
    site = repository.create_new(netdot.Site(name='Test Site'))
    caplog.set_level(logging.INFO)

    # Act
    repository.save_changes()

    # Assert
    assert_that(caplog.text).contains('Will CREATE Site')

    # Cleanup
    site.delete(confirm=False)


@pytest.mark.vcr
def test_incremental_creation_of_site_with_rooms(repository: Repository, caplog):
    # Arrange
    repository.enable_propose_changes(print_changes=False)
    site = repository.create_new(netdot.Site(name='Test Site'))
    floor = site.add_floor(netdot.Floor(level='Test Floor'))
    room1 = floor.add_room(netdot.Room(name='Test Room 1'))
    room2 = floor.add_room(netdot.Room(name='Test Room 2'))
    room3 = floor.add_room(netdot.Room(name='Test Room 3'))
    closet = room3.add_closet(netdot.Closet(name='Test Closet 1'))
    caplog.set_level(logging.INFO)

    # Act
    repository.save_changes()

    # Assert
    assert_that(site.id).is_not_none()
    assert_that(floor.id).is_not_none()
    assert_that(room1.id).is_not_none()
    assert_that(room2.id).is_not_none()
    assert_that(room3.id).is_not_none()
    assert_that(closet.id).is_not_none()

    # Cleanup
    site.delete(confirm=False)
