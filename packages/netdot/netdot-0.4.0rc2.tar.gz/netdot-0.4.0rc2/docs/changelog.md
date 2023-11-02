# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Notice: Major version zero (0.y.z) is for initial development. Anything MAY change at any time.
> This public API should **not** be considered stable.

> ⚠ Disclaimer: From 0.2.0 onward, this API wrapper does not ensure support for the [de facto Open Source version of NetDot (GitHub)](https://github.com/cvicente/Netdot).

## [Unreleased]

* After calling `save_changes`, `show_changes` does not show any of the completed tasks.
    * WORKAROUND: Calling `nd_repo.proposed_changes.completed_as_list()` will give the completed tasks.
* There are still 2 Python Dataclasses that just need to be implemented:
    - [ ] ARPCache
    - [ ] ARPCacheEntry 
* Retrieve/update various data types that contain **binary blobs** via REST API:
    - [ ] DataCaches
    - [ ] ClosetPictures
    - [ ] SitePictures
    - [ ] FloorPictures
* UnitOfWork has `dry_run` and `changes_as_table`, but does not have any `save_as` methods.
    * `save_as_excel` would be great to save all proposed changes as a workbook.
    * `save_as_csv` would be great to save all proposed changes as a set of CSV files.
    * `save_as` would be great to use Python's `pickle` serializer (paired with a `load` method to load it back up).


## [0.4.0]

### Added

* Generated some [API documentation](./generated.md) for all the generated code.
* Dry Runs!
    * See ['Example Plan and Create a New Netdot Site" in the User Guide](./user-guide.md#example-plan-and-create-a-new-netdot-site)
    * Automatically set up a UnitOfWork when calling `netdot.connect`
        > Bypass 'dry runs' feature via `netdot.connect_now` (or after the fact using `disable_propose_changes`)
    * Make changes just like normal (except calls to `create` will return objects **without** `id` populated)
    * Show any proposed changes using `show_changes`
        * Use `show_chages(terse=False)` to see full output.
        * Use `show_changes_as_tables` to see output as tables (which also supports the `terse=False` option)
    * Save those changes using `save_changes`
        * Asks for user confirmation for any DELETEs (unless `confirm=False` option is used)
* Implemented Python Dataclasses for *most* all of the Netdot Database schema
    * All except the four 'binary blob' containing data types, listed in [Unreleased](#unreleased).
* Basic methods on each NetdotAPIDataclass:
    * `create_or_update`: Create or update this object in Netdot.
    * `create`: *Thin wrapper around `create_or_update`.*
    * `update`: *Thin wrapper around `create_or_update`.*
    * `delete`: Delete this object in Netdot.
        * Asks for user confirmation (unless `confirm=False` option is used)
* Generate methods on each NetdotAPIDataclass:
    * `add_*` methods for 1-to-many relationships.
        * Examples: `site.add_device` or `site.add_sitelink_as_farend`
    * `add_*` methods for many-to-many relationships.
        * Examples: `site.add_subnet` (and the more obscure `site.add_sitesubnet`)
    * `load_*` methods for 1-to-many relationships.
        * Examples: `site.load_devices`
    * `load_*` methods for many-to-many relationships.
        * Examples: `site.load_subnets`
* [UNTESTED] Log a warning whenever 'Carp::croak' is returned in HTTP response.


### Changed

* Fix pluralization for various methods in [public API](./generated.md).
* Simplified NetdotAPIDataclass property setters (by overwriting `__setattr__` directly for NetdotAPIDataclass).
    * ❌ Old way:
    ```
    netdot.Floor(...).with_site(site)
    ```
    * ✅ New way, via `__init__`:
    ```
    floor = netdot.Floor(..., site=site, ...)
    ```
  * ✅ New way, via assignment operator (`=`):
    ```
    floor = netdot.Floor(...)
    floor.site = site
    ```

### Removed

* No longer generate the `with_*` and `set_*` methods for NetdotAPIDataclass.
* Do not log a warning when 'info' or 'ttl' are absent from HTTP Response (they are VERY optional)
    * Search for `inconsistent_and_ignorable_fields` to learn more
* Removed old `netdot.Connect` class entirely



## [0.3.2]

* Enable looking up a DNS Resource Record (RR) by address, using `repo.get_rr_by_address()`

## [0.3.1]

* Speed up `find_edge_port`.
  * HTTP requests are parallelized via multithreading where possible.

## [0.3.0]

> ⚠ Breaking Backwards Compatibility: Several `netdot.Repository` methods are renamed, as discussed below.

* Add `Repository.find_edge_port(mac_address)` method.
  * This requires a lot of HTTP requests since we do not have the ability to run arbitrary database queries (SQL JOIN behavior is unavailable via RESTful interface).
* Wired up the following netdot.dataclasses:
  * `ForwardingTable`
  * `ForwardingTableEntry`
  * `PhysAddr`
* Renamed several generated methods to end in "ies" instead of "ys" when pluralized.
* Dropping Python 3.6 and 3.7 compatibility (required to use [hatch](https://github.com/pypa/hatch))

## [0.2.6]

* Fix typo in `MACAddress:format` method argument: "delimeter" becomes "delimiter"
  * Additionally, force keyword arguments for the `format`using Python 3 feature.

## [0.2.5]

* In `netdot.Client` the base `delete(..., id)` method can now accept an `int`.
  * Before, it only accepted `str`.

## [0.2.4]

* Gracefully handle response from HTTP Delete requests when possible.
  * Delete seems to return 'empty' (a couple of newlines actually) on success.

## [0.2.3]

* Enable a `replace` function for all `netdot.dataclassess`
  * This makes it easier to do 'update' like operations using this library.

## [0.2.2]

* Fix for REGRESSION: The `post` method of `netdot.Client` does not work.
  * Debugged using a simple automated test (captured by a PyVCR Cassette for reproducibility)

## [0.2.1]

> 🐛 REGRESSION: The `post` method of `netdot.Client` does not work!

* Fix for REGRESSION: The `netdot.Client.Connection` class is missing!
  * Re-added `Connection` directly to client.py for now.
  * Aliased `netdot.client` module to also be available as it was formerly named, `netdot.Client` (pep8 suggests lowercase module names instead of CamelCase).
    * Using `__all__` in "netdot/\_\_init\_\_.py"

## [0.2.0]

> 🐛 REGRESSION: The `netdot.Client.Connection` class is MISSING!

> ⚠ We have not ensured support for the [de facto Open Source version of NetDot (GitHub)](https://github.com/cvicente/Netdot).

* Introducing a new layer of abstraction -- a Repository and many Python dataclasses.
  * See more info in the [User Guide](user-guide.md)
* Provide technical documentation in "docs/" directory (following NTS's standards).
  * See [the README.md in the &#34;docs/&#34; directory](README.md) for an overview.

## [0.1.0]

* Provide Python Netdot Client, as originally authored by Francisco Gray.
