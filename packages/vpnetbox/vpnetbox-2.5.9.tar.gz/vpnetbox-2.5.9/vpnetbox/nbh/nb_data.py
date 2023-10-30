"""NbData, Sets of Netbox objects, like aggregates, prefixes, etc., are joined together."""

from __future__ import annotations

import copy
from copy import deepcopy
from datetime import datetime

from vhelpers import vstr

from vpnetbox import NbParser
from vpnetbox.types_ import LDAny, ODatetime, DiDAny

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class NbData:  # pylint: disable=R0902
    """NbData, Sets of Netbox objects, like aggregates, prefixes, etc., are joined together."""

    _data_attrs = [
        # ipam
        "aggregates",
        # "asn_ranges",
        # "asns",
        "ip_addresses",
        "prefixes",
        "vlans",
        # dcim
        "devices",
        "sites",
        # circuits
        "circuit_types",
        "circuits",
        "providers",
        "circuit_terminations",
        # tenancy
        "tenant_groups",
        "tenants",
    ]
    _helper_attrs = [
        "name",
        "version",
        "last_update",
    ]

    def __init__(self, **kwargs):
        """Init NbData.

        ipam
        :param aggregates: List of Netbox ipam/aggregates objects.
        :param asn_ranges: List of Netbox ipam/asn-ranges objects.
        :param asns: List of Netbox ipam/asns objects.
        :param ip_addresses: List of Netbox ipam/ip-addresses objects.
        :param prefixes: List of Netbox ipam/prefixes objects.
        :param vlans: List of Netbox ipam/vlans objects.

        dcim
        :param sites: List of Netbox dcim/sites objects.
        :param devices: List of Netbox dcim/devices objects.

        circuits
        :param circuit_types: List of Netbox circuits/circuit_types objects.
        :param circuits: List of Netbox circuits/circuits objects.
        :param providers: List of Netbox circuits/providers objects.
        :param circuit_terminations: List of Netbox circuits/circuit-terminations objects.

        tenancy
        :param tenant_groups: List of Netbox tenancy/tenant-groups objects.
        :param tenants: List of Netbox tenancy/tenants objects.

        Other
        :param version: Netbox version.
        :param last_update: Last requested datetime (data age).
        """
        self.name = self._init_name(**kwargs)
        self.version: str = str(kwargs.get("version") or "0")
        self.last_update: ODatetime = _init_last_update(**kwargs)

        # LISTS
        # ipam
        self.aggregates: LDAny = list(kwargs.get("aggregates") or [])
        self.asn_ranges: LDAny = list(kwargs.get("asn_ranges") or [])
        self.asns: LDAny = list(kwargs.get("asns") or [])
        self.ip_addresses: LDAny = list(kwargs.get("ip_addresses") or [])
        self.prefixes: LDAny = list(kwargs.get("prefixes") or [])
        self.vlans: LDAny = list(kwargs.get("vlans") or [])
        # dcim
        self.devices: LDAny = list(kwargs.get("devices") or [])
        self.sites: LDAny = list(kwargs.get("sites") or [])
        # circuits
        self.circuit_types: LDAny = list(kwargs.get("circuit_types") or [])
        self.circuits: LDAny = list(kwargs.get("circuits") or [])
        self.providers: LDAny = list(kwargs.get("providers") or [])
        self.circuit_terminations: LDAny = list(kwargs.get("circuit_terminations") or [])
        # tenancy
        self.tenant_groups: LDAny = list(kwargs.get("tenant_groups") or [])
        self.tenants: LDAny = list(kwargs.get("tenants") or [])

        # RECURSIONS
        # ipam
        self.aggregates_d: DiDAny = {}
        self.asn_d: DiDAny = {}
        self.asn_ranges_d: DiDAny = {}
        self.ip_addresses_d: DiDAny = {}
        self.prefixes_d: DiDAny = {}
        self.vlans_d: DiDAny = {}
        # dcim
        self.devices_d: DiDAny = {}
        self.sites_d: DiDAny = {}
        # circuits
        self.circuit_types_d: DiDAny = {}
        self.circuits_d: DiDAny = {}
        self.providers_d: DiDAny = {}
        self.circuit_terminations_d: DiDAny = {}
        # tenancy
        self.tenant_groups_d: DiDAny = {}
        self.tenants_d: DiDAny = {}

    def __repr__(self) -> str:
        """__repr__."""
        params = vstr.repr_params(
            # ipam
            aggr=len(self.aggregates),
            asn=len(self.asns),
            asnr=len(self.asn_ranges),
            ipa=len(self.ip_addresses),
            pref=len(self.prefixes),
            vlan=len(self.vlans),
            # dcim
            dev=len(self.devices),
            site=len(self.sites),
            # circuits
            ctyp=len(self.circuit_types),
            cid=len(self.circuits),
            prov=len(self.providers),
            ter=len(self.circuit_terminations),
            # tenancy
            teng=len(self.tenant_groups),
            ten=len(self.tenants),
        )
        return f"<{self.name}: {params}>"

    def __copy__(self) -> NbData:
        """Copy."""
        nbd = NbData()
        nbd.version = self.version
        for attr in self._data_attrs:
            setattr(nbd, attr, deepcopy(getattr(self, attr)))
        return nbd

    # ============================= init =============================

    def _init_name(self, **kwargs) -> str:
        """Init name."""
        host = str(kwargs.get("host") or "")
        items = [self.__class__.__name__, host]
        items = [s for s in items if s]
        return " ".join(items)

    def join_objects(self) -> None:
        """Join Netbox objects within itself.

        Convert Netbox data lists to dict, where key is unique id.
        Create recursive links between objects.
        :return: None. Update self object.
        """
        self._init_dicts()
        # ipam
        self._join_aggregates()
        self._join_asn_ranges()
        self._join_asns()
        self._join_ip_addresses()
        self._join_prefixes()
        self._join_vlans()
        # dcim
        self._join_devices()
        self._join_sites()
        # circuits
        self._join_circuits()
        self._join_circuit_terminations()
        # tenancy
        self._join_tenant_groups()
        self._join_tenants()

    def _init_dicts(self) -> None:
        """Convert a list of Netbox objects into a dictionary where the key is the object ID.

        :return: None. Update self object.
        """
        for attr in self._data_attrs:
            items = getattr(self, attr)
            if not isinstance(items, list):
                raise TypeError(f"{attr} {list} expected")
            data = {int(d["id"]): d for d in deepcopy(items)}
            setattr(self, f"{attr}_d", data)

    def _join_aggregates(self):
        """Join aggregates.

        # todo
        rir
        tenant
        """

    def _join_asns(self):
        """Join asns.

        # todo
        rir
        tenant
        """

    def _join_asn_ranges(self):
        """Join asn_ranges.

        # todo
        rir
        """

    def _join_prefixes(self):
        """Join prefixes.

        # todo
        tenant
        role
        """

    def _join_ip_addresses(self):
        """Join ip-addresses.

        # todo
        tenant
        assigned_object
        """

    def _join_vlans(self):
        """Join vlans.

        # todo
        site
        group
        tenant
        role
        """

    def _join_devices(self):
        """Join devices: tenant, site.

        # todo
        device_type
        device_role
        platform

        location
        rack
        virtual_chassis
        """
        for device_d in self.devices_d.values():
            parser = NbParser(device_d)
            # tenant
            id_ = parser.int("tenant", "id")
            if tenant_d := self.tenants_d.get(id_) or {}:
                device_d["tenant"] = tenant_d
            # site
            id_ = parser.int("site", "id")
            if site_d := self.sites_d.get(id_) or {}:
                device_d["site"] = site_d

    def _join_sites(self):
        """Join sites.

        # todo
        region
        tenant
        asns
        """

    def _join_circuits(self):
        """Join circuits: provider, type, tenant, termination_a, termination_z."""
        for circuit_d in self.circuits_d.values():
            parser = NbParser(circuit_d)
            # provider
            id_ = parser.int("provider", "id")
            if provider_d := self.providers_d.get(id_) or {}:
                circuit_d["provider"] = provider_d
            # type
            id_ = parser.int("type", "id")
            if type_d := self.circuit_types_d.get(id_) or {}:
                circuit_d["type"] = type_d
            # tenant
            id_ = parser.int("tenant", "id")
            if tenant_d := self.tenants_d.get(id_) or {}:
                circuit_d["tenant"] = tenant_d
            # termination_a
            id_ = parser.int("termination_a", "id")
            if term_d := self.circuit_terminations_d.get(id_) or {}:
                circuit_d["termination_a"] = term_d
                term_d["circuit"] = circuit_d
            # termination_z
            id_ = parser.int("termination_z", "id")
            if term_d := self.circuit_terminations_d.get(id_) or {}:
                circuit_d["termination_z"] = term_d
                term_d["circuit"] = circuit_d

    def _join_circuit_terminations(self) -> None:
        """Join circuit-terminations: circuit, site, link_peers (devices).

        # todo
        cable
        """
        for term_d in self.circuit_terminations_d.values():
            parser = NbParser(term_d)
            # circuit
            id_: int = parser.int("circuit", "id")
            if circuit_d := self.circuits_d.get(id_) or {}:
                term_d["circuit"] = circuit_d
                if term_d["term_side"] == "A":
                    circuit_d["termination_a"] = term_d
                elif term_d["term_side"] == "Z":
                    circuit_d["termination_z"] = term_d
            # site
            id_ = parser.int("site", "id")
            if site_d := self.sites_d.get(id_) or {}:
                term_d["site"] = site_d
            # link_peers (devices)
            link_peers: LDAny = parser.list("link_peers")  # interfaces
            for interface_d in link_peers:
                parser_ = NbParser(interface_d)
                id_ = parser_.int("device", "id")
                if device_d := self.devices_d.get(id_) or {}:
                    interface_d["device"] = device_d

    def _join_tenant_groups(self) -> None:
        """Join tenant groups: parent."""
        for tenant_group_d in self.tenant_groups_d.values():
            parser = NbParser(tenant_group_d)
            # parent
            if id_ := parser.int("parent", "id"):
                if parent_d := self.tenant_groups_d.get(id_) or {}:
                    tenant_group_d["parent"] = parent_d

    def _join_tenants(self) -> None:
        """Join tenants: group."""
        for tenant_d in self.tenants_d.values():
            parser = NbParser(tenant_d)
            # group
            if id_ := parser.int("group", "id"):
                if group_d := self.tenant_groups_d.get(id_) or {}:
                    tenant_d["group"] = group_d

    # =========================== method =============================

    def copy(self) -> NbData:
        """Copy self object.

        :return: Copied NbData object.
        """
        return copy.copy(self)

    def clear(self) -> None:
        """Clear NbData."""
        self.version = "0"
        for attr in self._data_attrs:
            setattr(self, attr, [])

    def is_empty(self) -> bool:
        """Return True if NbData is empty (has no any data)."""
        return not any(getattr(self, s) for s in self._data_attrs)


# ============================= helpers ==============================

def _init_last_update(**kwargs) -> ODatetime:
    """Init time when data was requested last time.

    :return: Last updated datetime or None.
    """
    value = kwargs.get("last_updated")
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, DATE_FORMAT)
    if isinstance(value, int):
        return datetime.fromtimestamp(value)
    return None
