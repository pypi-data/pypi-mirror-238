"""IP Addresses Management."""
from vpnetbox.api.base import Base
from vpnetbox.types_ import LDAny


class Ipam:  # pylint: disable=R0902,R0903
    """IP Addresses Management."""

    def __init__(self, **kwargs):
        """Init Ipam."""
        self.aggregates = self.Aggregates(**kwargs)
        self.asn_ranges = self.AsnRanges(**kwargs)
        self.asns = self.Asns(**kwargs)
        self.fhrp_group_assignments = self.FhrpGroupAssignments(**kwargs)
        self.fhrp_groups = self.FhrpGroups(**kwargs)
        self.ip_addresses = self.IpAddresses(**kwargs)
        self.ip_ranges = self.IpRanges(**kwargs)
        self.l2vpn_terminations = self.L2vpnTerminations(**kwargs)
        self.l2vpns = self.L2vpns(**kwargs)
        self.prefixes = self.Prefixes(**kwargs)
        self.rirs = self.Rirs(**kwargs)
        self.roles = self.Roles(**kwargs)
        self.route_targets = self.RouteTargets(**kwargs)
        self.service_templates = self.ServiceTemplates(**kwargs)
        self.services = self.Services(**kwargs)
        self.vlan_groups = self.VlanGroups(**kwargs)
        self.vlans = self.Vlans(**kwargs)
        self.vrfs = self.Vrfs(**kwargs)

    class Aggregates(Base):
        """Aggregates."""

        def __init__(self, **kwargs):
            """Init Aggregates."""
            super().__init__(path="ipam/aggregates/", **kwargs)
            self._parallels.extend([
                "family",
                "prefix",
            ])

        def get(self, **kwargs) -> LDAny:
            """Get ipam/aggregates/ objects.

            WEB UI filter parameters
            ------------------------

            Data filter parameters
            ----------------------

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)

    class AsnRanges(Base):
        """AsnRanges."""

        def __init__(self, **kwargs):
            """Init AsnRanges."""
            super().__init__(path="ipam/asn-ranges/", **kwargs)

    class Asns(Base):
        """Asns."""

        def __init__(self, **kwargs):
            """Init Asns."""
            super().__init__(path="ipam/asns/", **kwargs)
            self._change_params = {
                "rir": {"query": "ipam/rirs/", "key": "name"},
                "site": {"query": "dcim/sites/", "key": "name"},
                "tenant": {"query": "tenancy/tenants/", "key": "name"},
                "tenant_group": {"query": "tenancy/tenant-groups/", "key": "name"},
            }

        # noinspection PyIncorrectDocstring
        def get(self, **kwargs) -> LDAny:
            """Get ipam/asns/ objects.

            WEB UI filter parameters
            ------------------------

            :param q: Search. ASN
            :type q: str or List[str]
            :example q: ["65001", "65002"]

            :param tag: Tag.
            :type tag: str or List[str]
            :example tag: ["alpha", "bravo"]

            :param rir: RIR.
            :type rir: str or List[str]
            :example rir: ["ARIN", "RFC 6996"]
            :param rir_id: RIR object ID.
            :type rir_id: int or List[int]
            :example rir_id: [1, 2]

            :param site: Site.
            :type site: str or List[str]
            :example site: ["SITE1", "SITE2"]
            :param site_id: Site object ID.
            :type site_id: int or List[int]
            :example site_id: [1, 2]

            :param tenant_group: Tenant group.
            :type tenant_group: str or List[str]
            :example tenant_group: ["TENANT GROUP1", "TENANT GROUP2"]
            :param tenant_group_id: Tenant group object ID.
            :type tenant_group_id: int or List[int]
            :example tenant_group_id: [1, 2]

            :param tenant: Tenant.
            :type tenant: str or List[str]
            :example tenant: ["TENANT1", "TENANT2"]
            :param tenant_id: Tenant object ID.
            :type tenant_id: int or List[int]
            :example tenant_id: [1, 2]

            Data filter parameters
            ----------------------

            :param id: Object ID.
            :type id: int or List[int]
            :example id: [1, 2]

            :param asn: ASN.
            :type asn: int or List[int]
            :example asn: [65001, 65002]

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)

    class FhrpGroupAssignments(Base):
        """FhrpGroupAssignments."""

        def __init__(self, **kwargs):
            """Init FhrpGroupAssignments."""
            super().__init__(path="ipam/fhrp-group-assignments/", **kwargs)

    class FhrpGroups(Base):
        """FhrpGroups."""

        def __init__(self, **kwargs):
            """Init FhrpGroups."""
            super().__init__(path="ipam/fhrp-groups/", **kwargs)

    class IpAddresses(Base):
        """IpAddresses."""

        def __init__(self, **kwargs):
            """Init IpAddresses."""
            super().__init__(path="ipam/ip-addresses/", **kwargs)
            self._sliced = "address"
            self._parallels.extend([
                "assigned_to_interface",
                "family",
                "mask_length",
                "parent",
            ])
            self._change_params = {
                "present_in_vrf": {"path": "ipam/vrfs/", "key": "name"},
                "tenant": {"path": "tenancy/tenants/", "key": "name"},
                "tenant_group": {"path": "tenancy/tenant-groups/", "key": "name"},
                "vrf": {"path": "ipam/vrfs/", "key": "name"},
            }

        # noinspection PyIncorrectDocstring
        def get(self, **kwargs) -> LDAny:
            """Get ipam/ip-addresses/ objects.

            Each filter parameter can be either a single value or a list of values.
            Different parameters work like 'AND' operator,
            while multiple values in the same parameter work like an 'OR' operator.
            Not all filter parameters are documented.
            Please refer to the Netbox API documentation for more details.

            WEB UI filter parameters
            ------------------------

            :param q: Search. Substring of ip address value.
            :type q: str or List[str]
            :example q: ["10.0.0.", "10.31.65."]

            :param tag: Tag.
            :type tag: str or List[str]
            :example tag: ["alpha", "bravo"]

            :param parent: Parent Prefix. Addresses that are part of this prefix.
            :type parent: str or List[str]
            :example parent: ["10.0.0.0/24", "10.31.65.0/26"]

            :param family: Address family. IP version.
            :type family: int or List[int]
            :example family: [4, 6]

            :param status: Status.
            :type status: str or List[str]
            :example status: ["active", "reserved"]

            :param role: Role.
            :type role: str or List[str]
            :example role: ["secondary", "hsrp"]

            :param mask_length: Mask length.
            :type mask_length: int or List[int]
            :example mask_length: [24, 32]

            :param assigned_to_interface: Assigned to an interface.
            :type assigned_to_interface: bool
            :example assigned_to_interface: True

            :param vrf: VRF.
            :type vrf: str or List[str]
            :example vrf: ["VRF1", "VRF2"]
            :param vrf_id: VRF object ID.
            :type vrf_id: int or List[int]
            :example vrf_id: [1, 2]

            :param present_in_vrf: Present in VRF.
            :type present_in_vrf: str or List[str]
            :example present_in_vrf: ["VRF1", "VRF2"]
            :param present_in_vrf_id: Present in VRF object ID.
            :type present_in_vrf_id: int or List[int]
            :example present_in_vrf_id: [1, 2]

            :param tenant_group: Tenant group.
            :type tenant_group: str or List[str]
            :example tenant_group: ["TENANT GROUP1", "TENANT GROUP2"]
            :param tenant_group_id: Tenant group object ID.
            :type tenant_group_id: int or List[int]
            :example tenant_group_id: [1, 2]

            :param tenant: Tenant.
            :type tenant: str or List[str]
            :example tenant: ["TENANT1", "TENANT2"]
            :param tenant_id: Tenant object ID.
            :type tenant_id: int or List[int]
            :example tenant_id: [1, 2]

            :param device: Assigned Device.
            :type device: str or List[str]
            :example device: ["DEVICE1", "DEVICE2"]
            :param device_id: Assigned Device object ID.
            :type device_id: int or List[int]
            :example device_id: [1, 2]

            :param virtual_machine: Assigned virtual machine.
            :type virtual_machine: str or List[str]
            :example virtual_machine: ["DEVICE1", "DEVICE2"]
            :param virtual_machine_id: Assigned virtual machine object ID.
            :type virtual_machine_id: int or List[int]
            :example virtual_machine_id: [1, 2]

            Data filter parameters
            ----------------------

            :param id: Object ID.
            :type id: int or List[int]
            :example id: [1, 2]

            :param address: IP Address.
            :type address: str or List[str]
            :example address: ["10.0.0.1/26", "10.0.0.2/26"]

            :param dns_name: DNS name.
            :type dns_name: str or List[str]
            :example dns_name: ["host1.domain.com", "host2.domain.com"]

            :param description: Description.
            :type description: str or List[str]
            :example description: ["TEXT1", "TEXT2"]

            :param created: Datetime when the object was created.
            :type created: str or List[str]
            :example created: ["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"]

            :param last_updated: Datetime when the object was updated.
            :type last_updated: str or List[str]
            :example last_updated: ["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"]

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)

    class IpRanges(Base):
        """IpRanges."""

        def __init__(self, **kwargs):
            """Init IpRanges."""
            super().__init__(path="ipam/ip-ranges/", **kwargs)

    class L2vpnTerminations(Base):
        """L2vpnTerminations."""

        def __init__(self, **kwargs):
            """Init L2vpnTerminations."""
            super().__init__(path="ipam/l2vpn-terminations/", **kwargs)

    class L2vpns(Base):
        """L2vpns."""

        def __init__(self, **kwargs):
            """Init L2vpns."""
            super().__init__(path="ipam/l2vpns/", **kwargs)

    class Prefixes(Base):
        """Prefixes."""

        def __init__(self, **kwargs):
            """Init Prefixes."""
            super().__init__(path="ipam/prefixes/", **kwargs)
            self._parallels.extend([
                "assigned_to_interface",
                "cf_env",
                "family",
                "mask_length",
                "prefix",
            ])

        def get(self, **kwargs) -> LDAny:
            """Get ipam/prefixes/ objects.

            WEB UI filter parameters
            ------------------------

            Data filter parameters
            ----------------------

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)

    class Rirs(Base):
        """Rirs."""

        def __init__(self, **kwargs):
            """Init Rirs."""
            super().__init__(path="ipam/rirs/", **kwargs)

    class Roles(Base):
        """Roles."""

        def __init__(self, **kwargs):
            """Init Roles."""
            super().__init__(path="ipam/roles/", **kwargs)

    class RouteTargets(Base):
        """RouteTargets."""

        def __init__(self, **kwargs):
            """Init RouteTargets."""
            super().__init__(path="ipam/route-targets/", **kwargs)

    class ServiceTemplates(Base):
        """ServiceTemplates."""

        def __init__(self, **kwargs):
            """Init ServiceTemplates."""
            super().__init__(path="ipam/service-templates/", **kwargs)

    class Services(Base):
        """Services."""

        def __init__(self, **kwargs):
            """Init Services."""
            super().__init__(path="ipam/services/", **kwargs)

    class VlanGroups(Base):
        """VlanGroups."""

        def __init__(self, **kwargs):
            """Init VlanGroups."""
            super().__init__(path="ipam/vlan-groups/", **kwargs)

    class Vlans(Base):
        """Vlans."""

        def __init__(self, **kwargs):
            """Init Vlans."""
            super().__init__(path="ipam/vlans/", **kwargs)

    class Vrfs(Base):
        """Vrfs."""

        def __init__(self, **kwargs):
            """Init Vrfs."""
            super().__init__(path="ipam/vrfs/", **kwargs)
