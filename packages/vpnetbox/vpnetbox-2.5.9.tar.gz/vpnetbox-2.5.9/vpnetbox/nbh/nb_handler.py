"""NbHandler.

Retrieves and caches a bulk of data from the Netbox to local system.
Collects sets of aggregates, prefixes, addresses, devices, sites data from Netbox
and saves it in NbData object.
"""

from __future__ import annotations

import copy
import logging
from pathlib import Path

from vpnetbox.messages import Messages
from vpnetbox.nb_api import NbApi
from vpnetbox.nb_parser import NbParser
from vpnetbox.nbh.cache import Cache
from vpnetbox.nbh.nb_data import NbData
from vpnetbox.types_ import LStr


class NbHandler:  # pylint: disable=R0904
    """Retrieves and caches a bulk of data from the Netbox to local system.

    Collects sets of aggregates, prefixes, addresses, devices, sites data from Netbox
    and saves it in NbData object.
    """

    def __init__(self, **kwargs):
        """Init NbHandler.

        Parameters for NbApi are described in the NbApi class in ../api/nb_api.py.
        Parameters for NbData are described in the NbData class in ./nb_data.py.
        Parameters for Cache are described in the Cache class in ../cache.py.
        """
        self.api = NbApi(**kwargs)
        self.nbd = NbData(**kwargs)
        cache_path: str = init_cache_path(name=self.__class__.__name__, **kwargs)
        self.cache = Cache(nbd=self.nbd, cache_path=cache_path)
        self.msgs = Messages(name=self.api.host)

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        nbd_name = self.nbd.__repr__()
        name = nbd_name.replace(self.nbd.__class__.__name__, name)
        return name

    def __copy__(self) -> NbHandler:
        """Copy NbApi object and all data in NbData object.

        :return: Copy of NbHandler object.
        """
        api_params = getattr(self.api.ipam.aggregates, "_init_params")
        params_d = {s: getattr(self.api.ipam.aggregates, s) for s in api_params}
        nbh = NbHandler(**params_d)
        nbh.nbd = self.nbd.copy()
        return nbh

    # ========================== scenarios ===========================

    def get_aggregates(self, **kwargs) -> None:
        """Get Netbox ipam/aggregates objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the Aggregates object.
        :return: None. Update self object.
        """
        self.nbd.aggregates = self.api.ipam.aggregates.get(**kwargs)

    def get_ip_addresses(self, **kwargs) -> None:
        """Get Netbox ipam/ip-addresses objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the IpAddresses object.
        :return: None. Update self object.
        """
        self.nbd.ip_addresses = self.api.ipam.ip_addresses.get(**kwargs)

    def get_prefixes(self, **kwargs) -> None:
        """Get Netbox ipam/prefixes objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the Prefixes object.
        :return: None. Update self object.
        """
        self.nbd.prefixes = self.api.ipam.prefixes.get(**kwargs)

    def get_vlans(self, **kwargs) -> None:
        """Get Netbox ipam/vlans objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the Vlans object.
        :return: None. Update self object.
        """
        self.nbd.vlans = self.api.ipam.vlans.get(**kwargs)

    def get_devices(self, **kwargs) -> None:
        """Get Netbox dcim/devices objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the Devices object.
        :return: None. Update self object.
        """
        self.nbd.devices = self.api.dcim.devices.get(**kwargs)

    def get_sites(self, **kwargs) -> None:
        """Get Netbox dcim/sites objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the Sites object.
        :return: None. Update self object.
        """
        self.nbd.sites = self.api.dcim.sites.get(**kwargs)

    def get_circuit_terminations(self, **kwargs) -> None:
        """Get Netbox circuits/terminations objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the Terminations object.
        :return: None. Update self object.
        """
        self.nbd.circuit_terminations = self.api.circuits.circuit_terminations.get(**kwargs)

    def get_circuit_types(self, **kwargs) -> None:
        """Get Netbox circuits/circuit-types objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the CircuitTypes object.
        :return: None. Update self object.
        """
        self.nbd.circuit_types = self.api.circuits.circuit_types.get(**kwargs)

    def get_circuits(self, **kwargs) -> None:
        """Get Netbox circuits/circuits objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the Circuits object.
        :return: None. Update self object.
        """
        self.nbd.circuits = self.api.circuits.circuits.get(**kwargs)

    def get_providers(self, **kwargs) -> None:
        """Get Netbox circuits/providers objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the Providers object.
        :return: None. Update self object.
        """
        self.nbd.providers = self.api.circuits.providers.get(**kwargs)

    def get_tenant_groups(self, **kwargs) -> None:
        """Get Netbox tenancy/tenant-groups objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the tenants object.
        :return: None. Update self object.
        """
        self.nbd.tenant_groups = self.api.tenancy.tenant_groups.get(**kwargs)

    def get_tenants(self, **kwargs) -> None:
        """Get Netbox tenancy/tenants objects by using the filter parameters in kwargs.

        :param kwargs: Filter parameters are described in the tenants object.
        :return: None. Update self object.
        """
        self.nbd.tenants = self.api.tenancy.tenants.get(**kwargs)

    # =========================== method =============================

    def clear(self) -> None:
        """Delete all data in NbData.

        :return: None. Update self object.
        """
        self.nbd.clear()

    def copy(self) -> NbHandler:
        """Copy NbApi and NbData objects.

        :return: Copied NbHandler object.
        """
        return copy.copy(self)

    def is_empty(self) -> bool:
        """Check if all NbData data attributes are empty.

        :return: True if NbData is empty, otherwise Else.
        """
        return self.nbd.is_empty()

    def read_cache(self) -> None:
        """Read cached data from a pickle file and restore recursions in Net objects.

        :return: None. Update self object.
        """
        self.cache.read_cache()
        self.nbd.join_objects()

    def write_cache(self) -> None:
        """Write cache to a pickle file..

        :return: None. Update a pickle file.
        """
        self.cache.write_cache()

    def join_objects(self) -> None:
        """Join Netbox objects within itself.

        Convert Netbox data lists to dict, where key is unique id.
        Create recursive links between objects.
        :return: None. Update self object.
        """
        self.nbd.join_objects()

    # noinspection PyProtectedMember
    def print_warnings(self) -> None:
        """Print WARNINGS if found some errors/warnings in data processing."""
        data_attrs = self.nbd._data_attrs  # pylint: disable=protected-access
        data_lists = [getattr(self.nbd, s) for s in data_attrs]
        for datas in data_lists:
            for data in datas:
                if warnings := data.get("warnings") or []:
                    for msg in warnings:
                        logging.warning(msg)

    # =========================== data methods ===========================

    def devices_primary_ip4(self) -> LStr:
        """Return the primary IPv4 addresses of Netbox devices with these settings.

        :return: primary_ip4 addresses of devices.
        """
        parsers = [NbParser(data=d) for d in self.nbd.devices]
        ip4s: LStr = sorted({o.primary_ip4() for o in parsers})
        ip4s = [s for s in ip4s if s]
        return ip4s

    def set_addresses_mask_32(self) -> None:
        """Change mask to /32 for all Netbox addresses.

        :return: None. Update self object.
        """
        for nb_addr in self.nbd.ip_addresses:
            address = nb_addr["address"]
            nb_addr["address"] = address.split("/")[0] + "/32"


# ============================= helpers =============================

# noinspection PyIncorrectDocstring
def init_cache_path(var: str = "", **kwargs) -> str:
    """Make path to pickle file.

    :param var: Pat to var directory.
    :param name: Parent object name.
    :param host: Netbox host name.
    :return: Path to cache pickle file.
    """
    if var.endswith(".pickle"):
        return var
    name = str(kwargs.get("name") or "")
    host = str(kwargs.get("host") or "")
    file_name_l = [name, host, "pickle"]
    file_name_l = [s for s in file_name_l if s]
    name = ".".join(file_name_l)
    path = Path(var, name)
    return str(path)
