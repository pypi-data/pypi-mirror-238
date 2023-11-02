
vpnetbox
=========

Python package to work with Netbox using REST API.
Facilitates low-level calls to Netbox and data parsing.

- NbApi: Requests data from the Netbox REST API using filter parameters identical to those in the web interface filter form.
- NbParser: Extracts a value from a Netbox object using a long chain of keys.
- NbHandler: Retrieves and caches a bulk of data from the Netbox to local system.
- NbData: Sets of Netbox objects, like aggregates, prefixes, etc., are joined together.

`./docs/NbHandler_diagram.rst`_

.. contents::


Introduction
------------
I am a network engineer and my scripts are designed to resolve network issues when the network is down.
I am facing some coding challenges where the speed and stability of my script are crucial, which is why I decided to stop using Pynetbox and start this project.
So, what is the utility of this tool? In short, I aim to make my scripts easier, more stable and faster.
In detail:

- Filtering. The 'get' methods provide filter parameters that are similar to those in the Netbox Web UI (for example, 'tenant' instead of 'tenant_id'). With 'get' parameters, you can implement filtering similar 'AND' and 'OR' operators.
- Tests. Code based on the REST API is much easier to cover with tests, because the Netbox returns a simple dictionary, which is easy to mock (testing code based on Pynetbox presents a challenge).
- Cache. Vpnetbox can save Netbox objects to a pickle file and work with them locally. Your script can work with Netbox data when the Netbox API is unreachable.
- Speed. Using Vpnetbox you can retrieve a bulk of data faster than when using Pynetbox (it maintains a connection with Netbox and downloads additional data during processing, which makes the script run veeeery slowly). Typically, I download a large amount of data to my local system, save it to cache and then start processing.


Requirements
------------

Python >=3.8


Installation
------------

Install the package from pypi.org release

.. code:: bash

    pip install vpnetbox

or install the package from github.com release

.. code:: bash

    pip install https://github.com/vladimirs-git/vpnetbox/archive/refs/tags/2.5.11.tar.gz

or install the package from github.com repository

.. code:: bash

    pip install git+https://github.com/vladimirs-git/vpnetbox


Usage
-----
For more details, please refer to the `./examples`_ directory where you will find numerous examples.

To get started, use the following example.

.. code:: python

    HOST = "demo.netbox.dev"
    TOKEN = "*****"
    nb = NbApi(host=HOST, token=TOKEN)

    # Create addresses
    response = nb.ip_addresses.create(address="10.1.1.1/24", tags=[1], status="reserved")
    print(response)  # <Response [201]>
    response = nb.ip_addresses.create(address="10.1.1.1/24", tags=[2], vrf=2)
    print(response)  # <Response [201]>

    # Get all addresses
    addresses = nb.ip_addresses.get()
    print(len(addresses))  # 181

    # Simple filter
    addresses = nb.ip_addresses.get(vrf="none")
    print(len(addresses))  # 30
    addresses = nb.ip_addresses.get(tag=["alpha", "bravo"])
    print(len(addresses))  # 4

    # Complex filter. Get addresses that do not have VRF and have either the tag 'alpha' or 'brave'
    # and have a status of either active or reserved.
    addresses = nb.ip_addresses.get(vrf="none", tag=["alpha", "bravo"], status=["active", "reserved"])
    print(len(addresses))  # 1

    addresses = nb.ip_addresses.get(address="10.1.1.1/24")
    for address in addresses:
        # Update
        id_ = address["id"]
        response = nb.ip_addresses.update(id=id_, description="text")
        print(response)  # <Response [200]>
        print(nb.ip_addresses.get(id=id_)[0]["description"])  # text

        # Delete
        response = nb.ip_addresses.delete(id=id_)
        print(response)  # <Response [204]>

Example of threading mode.

.. code:: python

    import logging
    from datetime import datetime
    from vpnetbox import NbApi

    # Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

    HOST = "demo.netbox.dev"
    TOKEN = "*****"

    # Get a lot of data in threading mode.
    start = datetime.now()
    nb = NbApi(host=HOST, token=TOKEN, threads=10, interval=0.1)
    objects = nb.ip_addresses.get()
    seconds = (datetime.now() - start).seconds
    print([d["address"] for d in objects])
    print(f"{len(objects)=} {seconds=}")
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/?brief=1&limit=1 ...
    # DEBUG    Starting new HTTPS connection (2): demo.netbox.dev:443
    # DEBUG    Starting new HTTPS connection (3): demo.netbox.dev:443
    # DEBUG    Starting new HTTPS connection (4): demo.netbox.dev:443
    # DEBUG    Starting new HTTPS connection (5): demo.netbox.dev:443
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # len(objects)=4153 seconds=3


NbApi
=====
NbApi, Python wrapper of Netbox REST API. Requests data from the Netbox REST API using filter parameters.

* Multithreading is used to request a bulk of data in fast mode.
* In 'get' method you can use multiple filter parameters. Different parameters work like 'AND' operator, while multiple values in the same parameter work like an 'OR' operator.
* Retries the request multiple times if the Netbox API responds with a timed-out. This is useful for scheduled scripts in cron jobs, when the connection to Netbox server is not stable.
* Slices the query to multiple requests if the URL length exceeds 4000 characters (due to a long list of GET parameters).
* Replaces an error-400 response with an empty result. For example, when querying addresses by tag, if there are no address objects with this tag in Netbox, the default Netbox API response is error-400. This package logs a warning and returns an ok-200 response with an empty list.

All connectors (ipam.ip_addresses, dcim.devices, etc.) have 'get', 'create', 'update' and 'delete' methods.
The 'create', 'update' and 'delete' methods are identical for all connectors,
but the parameters for the 'get' method are different for each connector.
Only 'ipam.ip_addresses' is fully described in the README, but other connectors are implemented in a similar manner.
To find available filter parameters for other connectors, you can use the Netbox Web UI filter page,
code docstrings, `./examples`_ or simply try your luck and experiment.


NbApi Parameters
----------------

=========== ======= ================================================================================
Parameter   Type    Description
=========== ======= ================================================================================
host        *str*   Netbox host name.
token       *str*   Netbox token.
scheme      *str*   Access method: https or http. Default https.
verify      *bool*  Transport Layer Security. True - A TLS certificate required, False - Requests will accept any TLS certificate.
limit       *int*   Split the query to multiple requests if the response exceeds the limit. Default 1000.
threads     *int*   Threads count. Default 1, loop mode.
interval    *int*   Wait this time between requests (seconds). Default 0. Useful for request speed shaping.
max_items   *int*   Stop the request if received items reach this value. Default unlimited. Useful if you need many objects but not all.
timeout     *float* Request timeout (seconds). Default 60.
max_retries *int*   Retry the request multiple times if it receives a 500 error or timed-out. Default 3.
sleep       *float* Interval before the next retry after receiving a 500 error (seconds). Default 10.
url_max_len *int*   Split the query to multiple requests if the URL length exceeds this value. Default ~3900.
=========== ======= ================================================================================


NbApi Methods
-------------


create(\*\*params)
------------------
Create object in Netbox.

=========== ====== =================================================================================
Parameter   Type   Description
=========== ====== =================================================================================
params      *dict* Parameters of new object.
=========== ====== =================================================================================

Return
      *Response* Session response. *<Response [201]>* Object successfully created, *<Response [400]>* Object already exist.


create_d(\*\*params)
--------------------
Create object in Netbox.

=========== ====== =================================================================================
Parameter   Type   Description
=========== ====== =================================================================================
params      *dict* Parameters of new object.
=========== ====== =================================================================================

Return
      *DAny* Dictionary of crated object.


update(\*\*params)
------------------
Update object in Netbox.

=========== ====== =================================================================================
Parameter   Type   Description
=========== ====== =================================================================================
params      *dict* Parameters to update object in Netbox, id is required.
=========== ====== =================================================================================

Return
      *Response* Session response. *<Response [200]>* Object successfully updated, *<Response [400]>* Invalid data.


update_d(\*\*params)
--------------------
Update object in Netbox.

=========== ====== =========================================================================================
Parameter   Type   Description
=========== ====== =========================================================================================
params      *dict* Parameters to update object in Netbox, id is required.
=========== ====== =========================================================================================

Return
      *DAny* Dictionary of updated object.


delete(id)
----------
Delete object in Netbox.

=========== ====== =================================================================================
Parameter   Type   Description
=========== ====== =================================================================================
id          *int*  Object unique identifier.
=========== ====== =================================================================================

Return
      *Response* Session response. *<Response [204]>* Object successfully deleted, *<Response [404]>* Object not found.


ip_address.get(\*\*params)
--------------------------
Get ipam/ip-addresses/ objects. Each filter parameter can be either a single value or a list of
values. Different parameters work like 'AND' operator, while multiple values in the same parameter
work like an 'OR' operator. Not all filter parameters are documented. Please refer to the Netbox API
documentation for more details.


===================== ==================== =========================================================
Parameter             Type                 Description
===================== ==================== =========================================================
**WEB UI FILTERS**    - - - - - -          - - - - - - - - -
q                     *str* or *List[str]* IP address substring.
tag                   *str* or *List[str]* Tag.
parent                *str* or *List[str]* Parent Prefix. Addresses that are part of this prefix.
family                *int* or *List[int]* Address family. IP version.
status                *str* or *List[str]* Status.
role                  *str* or *List[str]* Role.
mask_length           *int* or *List[int]* Mask length.
assigned_to_interface *bool*               Assigned to an interface.
vrf                   *str* or *List[str]* VRF.
vrf_id                *int* or *List[int]* VRF object ID.
present_in_vrf        *str* or *List[str]* Present in VRF.
present_in_vrf_id     *int* or *List[int]* Present in VRF object ID.
tenant_group          *str* or *List[str]* Tenant group.
tenant_group_id       *int* or *List[int]* Tenant group object ID.
tenant                *str* or *List[str]* Tenant.
tenant_id             *int* or *List[int]* Tenant object ID.
device                *str* or *List[str]* Assigned Device.
device_id             *int* or *List[int]* Assigned Device object ID.
virtual_machine       *str* or *List[str]* Assigned virtual machine.
virtual_machine_id    *int* or *List[int]* Assigned virtual machine object ID.
**DATA FILTERS**      - - - - - -          - - - - - - - - -
id                    *int* or *List[int]* Object ID.
address               *str* or *List[str]* IP Address.
dns_name              *str* or *List[str]* DNS name.
description           *str* or *List[str]* Description.
created               *str* or *List[str]* Datetime when the object was created.
last_updated          *str* or *List[str]* Datetime when the object was updated.
===================== ==================== =========================================================

Return
      *List[dict]* List of found objects.


NbParser
========
`./docs/NbParser.rst`_
Extracts the values from a Netbox object using a chain of keys.


NbHandler
=========
`./docs/NbHandler.rst`_
Retrieves and caches a bulk of data from the Netbox to local system.
Collects sets of aggregates, prefixes, addresses, devices, sites data from Netbox by scenarios.
(This handler is not yet finished, and I plan to improve it.)


.. _`./docs/NbHandler.rst`: ./docs/NbHandler.rst
.. _`./docs/NbHandler_diagram.rst`: ./docs_/NbHandler_diagram.rst
.. _`./docs/NbParser.rst`: ./docs/NbParser.rst
.. _`./examples`: ./examples
