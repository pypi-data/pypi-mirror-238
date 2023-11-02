A python wrapper for UO-NetDot's RESTful API.

> ⚠ Disclaimer: From 0.2.0 onward, this API wrapper does not ensure support for the [de facto Open Source version of NetDot (GitHub)](https://github.com/cvicente/Netdot).

[![PyPI version](https://badge.fury.io/py/netdot.svg)](https://badge.fury.io/py/netdot)

# Install 

This package is deployed to pypi.org.
Download it with `pip`:

    pip install netdot

# Interactive Usage (Python interpreter)

Before getting into building a massive integration/tool, you might jump in and get some experience.
Thankfully, we have the [Python 3 Interpreter (external)](https://docs.python.org/3/tutorial/interpreter.html) where we can jump in and do some testing!

    # Enter the Python interpreter by running just "python" in your shell
    $ python
    Python 3.8.10 (default, May 26 2023, 14:05:08)     
    ... omitted for brevity...
    >>> import netdot
    >>>

> ℹ The Python interpreter is often referred to as 'a REPL' (Read-Eval-Print-Loop).
> If you are unfamiliar with the Python interpreter, aka 'REPL', you might want to get started by reading ["Using the REPL (in VSCode)" documentation](https://www.learnpython.dev/01-introduction/02-requirements/05-vs-code/04-the-repl-in-vscode/).

With the netdot package imported, you can proceed with setting up a connecting and downloading some data!

> ℹ Many methods of `netdot.Repository` and `netdot.dataclasses` are actually runtime-generated code (well documented in our [API documentation](./generated.md)).
> Using the Repository interactively at the interpreter allows using features like **tab completion**. 

## Connecting in the interpreter: `netdot.connect()`

We have enabled interpreter-usage as a first-class feature.
In particular, you will want to use the `connect` function like the following.

> ℹ `netdot.connect()` returns a `netdot.Repository` instance.

    >>> import netdot
    >>> nd_repo = netdot.connect()
    What is the URL of the NetDot server? [https://nsdb.uoregon.edu]: ('enter' to use default)
    NetDot username: myusername
    NetDot password: ********** (using getpass module, to securely collect password)
    >>> 

We now have a `netdot.Repository` named `nd_repo` connected to netdot!

### Example: Lookup IP Address

As an example, you can use this API to lookup an IP Address.

    >>> ipaddr = nd_repo.get_ipblock_by_address('128.223.61.69')

Lets assume we want to determine who all may depend on this IP Address.
We'll see if we can discover useful information from the `used_by` field of this IP Address, or its parent(s)...

    >>> ipaddr.used_by
    None
    >>> subnet = ipaddr.get_parent()
    >>> subnet.used_by
    'Network & Telecom Services'
    >>> ip_container = subnet.get_parent()
    >>> ip_container.used_by
    'University of Oregon (3582)'

Perhaps it is more useful to look at the info

> ℹ Similar to `get_parent`, there is also a `get_children` method.

### Example: Lookup DNS Record by Address 

You can use this API to lookup the DNS Resource Record (RR) associated to some IP Address.

    >>> dns_record = nd_repo.get_rr_by_address('128.223.37.93')

The RR contains several pieces of information that may be useful!

    >>> dns_record.info
    'LOC: 123 FooBar Hall CON: Jenny J, 867-5309'

### Example: Lookup Edge Port for MAC Address in NetDot

> **⚠ WARNING**: "find_edge_port" includes assumptions that can result in inaccurate results.
> See full warning at end of this section for more info.

As an example, you can use this API to lookup the Edge Port associated to some MAC Address.

> ℹ Tip: This is useful for tracking down the physical location of some MAC Address.
> 
> ℹ This requires a LOT of HTTP requests.
> HTTP requests can be  [parallelized via multithreading (discussed below)](#multithreading-for-parallelizing-http-requests).

    >>> interface = nd_repo.find_edge_port('8C3BADDA9EF1')

Once the interface lookup is complete (may take more than 60 seconds), it is very easy to check if there is any "`jack`" (location information) associated to this Interface!

    >>> interface.jack
    '146A010B'

> **⚠ WARNING**: "find_edge_port" includes assumptions that can result in inaccurate results. 
> (This issue is present when looking up an edge port using NetDot's frontend as well)
> 
> Particularly, **if more than one forwarding table contains the MAC Address**, then NetDot will select the one whose forwarding table had the least entries.
>
> This can be inaccurate especially if a forwarding table scan is happening while trying to `find_edge_port`.

### Example: Load All Devices for a Site

Want to see all the devices that are located within the Site named "Death Star?"

First lookup the site:

    >>> site_name = 'Death Star'
    >>> sites = nd_repo.get_sites_where(name=site_name)
    >>> assert len(sites) == 1, f"Expected exactly one site with name {site_name}, found: {sites}"
    >>> site = sites[0]

Then, simply call "load_devices" on that site!

    >>> devices = site.load_devices()

### Example: Delete All Devices for a Site

**Continuing from the last example,** imagine 'Death Star' has been fully removed from your campus (pesky rebels).
You now want to go ahead and delete all the devices associated to this site.

    >>> for device in devices:
    >>>     device.delete()

The work has been prepared!
Take a look at what changes will occur using `show_changes` on the Repository object.

    >>> nd_repo.show_changes()
    ...    1. Will DELETE Device: Device(id=123, site_xlink=...
    ...    2. Will DELETE Device: Device(id=9000, site_xlink=...

If the deletes all look good, then go ahead and commit them using `save_changes`.

    >>> nd_repo.save_changes()

### Example: `show_changes` and `show_changes_as_tables`

Continuing from the prior example, we now know that `show_changes` will show exactly what will happen, step by step.

If you want a higher level overview of what is going to happen, you can use `show_changes_as_tables`:

    >>> nd_repo.show_changes_as_tables()
    ... 
    ... # TODO


> For an exceptionally small screen, you might like to use the following custom settings, to further truncate the cells of data printed to the screen.
> ```
> export NETDOT_CLI_TERSE_COL_WIDTH=8  # default is 16
> export NETDOT_CLI_TERSE_MAX_CHARS=16 # default is 64 (4*NETDOT_CLI_TERSE_COL_WIDTH)
> ```

### Example: Plan and Create a new Netdot Site
<a id='example-plan-and-create-a-new-netdot-site'></a>

Imagine you want to add a new site in Netdot, with rooms and all.

Assume that we are adding "Test Site," a simple site with just 1 floor, 3 rooms, and 1 closet.
Create all these objects within your dry run:

    >>> site =  nd_repo.create_new(netdot.Site(name='Test Site'))
    Will CREATE Site: Site(id=None, name='Test Site', aliases=None,
    >>> floor = site.add_floor(netdot.Floor(level='Test Floor'))
    Will CREATE Floor: Floor(id=None, info=None, level='Test Floor'
    >>> room1 = floor.add_room(netdot.Room(name='Test Room 1'))
    Will CREATE Room: Room(id=None, floor=Floor(id=None, info=None,
    >>> room2 = floor.add_room(netdot.Room(name='Test Room 2'))
    Will CREATE Room: Room(id=None, floor=Floor(id=None, info=None,
    >>> room3 = floor.add_room(netdot.Room(name='Test Room 3'))
    Will CREATE Room: Room(id=None, floor=Floor(id=None, info=None,
    >>> closet = room3.add_closet(netdot.Closet(name='Test Closet 1'))
    Will CREATE Closet: Closet(id=None, access_key_type=None, asbes

Then, confirm that the changes look good.

    >>> nd_repo.show_changes()
    1. Will CREATE Site: Site(id=None, name='Test Site', aliases=None, availability=None, availability_xlink=None, contactlist=
    2. Will CREATE Floor: Floor(id=None, info=None, level='Test Floor', site=Site(id=None, name='Test Site', aliases=None, avai
    3. Will CREATE Room: Room(id=None, floor=Floor(id=None, info=None, level='Test Floor', site=Site(id=None, name='Test Site',
    4. Will CREATE Room: Room(id=None, floor=Floor(id=None, info=None, level='Test Floor', site=Site(id=None, name='Test Site',
    5. Will CREATE Room: Room(id=None, floor=Floor(id=None, info=None, level='Test Floor', site=Site(id=None, name='Test Site',
    6. Will CREATE Closet: Closet(id=None, access_key_type=None, asbestos_tiles=False, catv_taps=None, converted_patch_panels=F


    nd_repo.save_changes()



## Automation Examples

The examples until now have all focused on the user running code directly in the Python Interpreter.
The remainder of the examples are 

### Example: Connecting using Environment Variables

For starters, we need to set up a `Repository` to interact with NetDot.
Environment variables can be a good method for providing credentials to your script, as suggested here:

> ℹ This pairs nicely with Continuous Integration! 
> It also works well enough for local development using [python-dotenv](https://pypi.org/project/python-dotenv/) or similar.

    import os
    import netdot

    nd_repo = netdot.Repository(
        netdot_url=os.getenv('NETDOT_URL'), 
        user=os.getenv('NETDOT_USERNAME'), 
        password=os.getenv('NETDOT_PASSWORD'),
    )

### Example: Update 'aliases' of Sites in NetDot

As a simple script example, imagine we want to update the 'aliases' with the string "(odd layout)" for some set of sites in NetDot.
In this example, we will write a script to do just that.

> For those who want to just see the script, there is the [full code sample below](#code-sample-for-example-update-aliases-of-sites-in-netdot)

Now, we are given a list of `SITE_IDS` to which we want to update the 'alias' with the string "(odd layout)".

    SITE_IDS = [98, 124, 512, 123, 111]

We can use Python list comprehensions to download the sites, and make the updates locally.

    sites = [ nd_repo.get_site(id) for id in SITE_IDS ]
    updated_sites = [ site.aliases=f'{site.aliases}(odd layout)' for site in sites ]

Then, it is time to apply the updates to the repository.

    for updated_site in updated_sites:
        updated_site.update()

Assuming that the repository is running in DRY RUN mode, then finalize the 

    nd_repo.save_changes()

#### Code Sample for Example: Update 'aliases' of Sites in NetDot

The full code sample is provided here.

    import netdot

    repo = netdot.Repository(...)  # Provide credentials, e.g. via environment variables using `os` module

    SITE_IDS = [98, 124, 512, 123, 111]
    sites = [ nd_repo.get_site(id) for id in SITE_IDS ]
    updated_sites = [ site.aliases=f'{site.aliases}(odd layout)' for site in sites ]

    for updated_site in updated_sites:
        updated_site.create_or_update()

## Multithreading for Parallelizing HTTP GET Requests

The `netdot.Repository` class can multithread HTTP requests.

To enable this, set the `NETDOT_CLI_THREADS` Environment Variable before running your python code.

    export NETDOT_CLI_THREADS=4

You can override this number by passing the `threads` keyword argument to the Repository constructor.

    >>> repo = netdot.Repository(..., threads=4)

> This `threads` keyword argument can be used in the [interactive interface (discussed above)](#interactive-usage-python-interpreter) as well.
> 
>     >>> repo = netdot.connect(threads=4)
