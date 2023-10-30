"""Circuits Management."""

from vpnetbox.api.base import Base
from vpnetbox.types_ import LDAny


class CircuitsM:  # pylint: disable=R0902,R0903
    """Circuits Management."""

    def __init__(self, **kwargs):
        """Init CircuitsM."""
        self.circuit_terminations = self.CircuitTerminations(**kwargs)
        self.circuit_types = self.CircuitTypes(**kwargs)
        self.circuits = self.Circuits(**kwargs)
        self.provider_accounts = self.ProviderAccounts(**kwargs)
        self.provider_networks = self.ProviderNetworks(**kwargs)
        self.providers = self.Providers(**kwargs)

    class CircuitTerminations(Base):
        """CircuitTerminations."""

        def __init__(self, **kwargs):
            """Init Terminations."""
            super().__init__(path="circuits/circuit-terminations/", **kwargs)
            self._change_params = {
                "cid": {"path": "circuits/circuits/", "key": "cid"},
                "site": {"path": "dcim/sites/", "key": "name"},
            }

        # noinspection PyIncorrectDocstring
        def get(self, **kwargs) -> LDAny:
            """Get circuits/circuit-terminations/ objects.

            WEB UI Filter parameters
            ------------------------

            Data Filter parameters
            ----------------------

            :param id: Object ID.
            :type id: int or List[int]
            :example id: [1, 2]

            :param cid: Circuit ID.
            :type cid: str or List[str]
            :example cid: ["CID1", "CID2"]
            :param circuit_id: Circuit object ID.
            :type circuit_id: int or List[int]
            :example circuit_id: [1, 2]

            :param site: Site name.
            :type site: str or List[str]
            :example site: ["FRA1", "FFL1"]
            :param site_id: Site object ID.
            :type site_id: int or List[int]
            :example site_id: [1, 2]

            :param port_speed: Port speed.
            :type port_speed: int or List[int]
            :example port_speed: [100000, 1000000]

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)

    class CircuitTypes(Base):
        """CircuitTypes."""

        def __init__(self, **kwargs):
            """Init CircuitTypes."""
            super().__init__(path="circuits/circuit-types/", **kwargs)

        # noinspection PyIncorrectDocstring
        def get(self, **kwargs) -> LDAny:
            """Get circuits/circuit-types/ objects.

            WEB UI Filter parameters
            ------------------------

            :param q: Search. Substring of circuit type name.
            :type q: str or List[str]
            :example q: ["DIA", "WAN"]

            Data Filter parameters
            ----------------------

            :param id: Object ID.
            :type id: int or List[int]
            :example id: [1, 2]

            :param name: Circuit type name.
            :type name: str or List[str]
            :example name: ["PROVIDER1", "PROVIDER2"]

            :param slug: Circuit type slug.
            :type slug: str or List[str]
            :example slug: ["provider1", "provider2"]

            :param tag: Tag.
            :type tag: str or List[str]
            :example tag: ["alpha", "bravo"]

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)

    class Circuits(Base):
        """Circuits."""

        def __init__(self, **kwargs):
            """Init Circuits."""
            super().__init__(path="circuits/circuits/", **kwargs)
            self._change_params = {
                "provider": {"path": "circuits/providers/", "key": "name"},
                "provider_account": {"path": "circuits/provider-accounts/", "key": "name"},
                "region": {"path": "dcim/regions/", "key": "name"},
                "site": {"path": "dcim/sites/", "key": "name"},
                "site_group": {"path": "dcim/site-groups/", "key": "name"},
                "tenant": {"path": "tenancy/tenants/", "key": "name"},
                "tenant_group": {"path": "tenancy/tenant-groups/", "key": "name"},
                "type": {"path": "circuits/circuit-types/", "key": "name"},
            }

        # noinspection PyIncorrectDocstring
        def get(self, **kwargs) -> LDAny:
            """Get circuits/circuits/ objects.

            WEB UI Filter parameters
            ------------------------

            :param q: Search. Substring of circuit ID.
            :type q: str or List[str]
            :example q: ["CID1", "CID2"]

            :param tag: Tag.
            :type tag: str or List[str]
            :example tag: ["alpha", "bravo"]

            :param provider: Provider name.
            :type provider: str or List[str]
            :example provider: ["PROVIDER1", "PROVIDER2"]
            :param provider_id: Provider object ID.
            :type provider_id: int or List[int]
            :example provider_id: [1, 2]

            :param provider_account: Provider account.
            :type provider_account: str or List[str]
            :example provider_account: ["PROVIDER1", "PROVIDER2"]
            :param provider_account_id: Provider account object ID.
            :type provider_account_id: int or List[int]
            :example provider_account_id: [1, 2]

            :param type: Circuit type.
            :type type: str or List[str]
            :example type: ["WAN", "DIA"]
            :param type_id: Circuit type object ID.
            :type type_id: int or List[int]
            :example type_id: [1, 2]

            :param status: Circuit status.
            :type status: str or List[str]
            :example status: ["active", "offline"]

            :param region: Region.
            :type region: str or List[str]
            :example region: ["USA", "EU"]
            :param region_id: Region object ID.
            :type region_id: int or List[int]
            :example region_id: [1, 2]

            :param site_group: Site group.
            :type site_group: str or List[str]
            :example site_group: ["FRA", "FFL"]
            :param site_group_id: Site group object ID.
            :type site_group_id: int or List[int]
            :example site_group_id: [1, 2]

            :param site: Site name.
            :type site: str or List[str]
            :example site: ["FRA1", "FFL1"]
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

            :param cf_monitoring_ip: Custom fields.
            :type cf_monitoring_ip: str or List[str]
            :example cf_monitoring_ip: ["10.0.0.1", "10.0.0.2"]

            Data Filter parameters
            ----------------------

            :param id: Object ID.
            :type id: int or List[int]
            :example id: [1, 2]

            :param cid: Circuit ID.
            :type cid: str or List[str]
            :example cid: ["CID1", "CID2"]

            :return: List of circuit objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)

    class ProviderAccounts(Base):
        """ProviderAccounts."""

        def __init__(self, **kwargs):
            """Init ProviderAccounts."""
            super().__init__(path="circuits/provider-accounts/", **kwargs)

    class ProviderNetworks(Base):
        """ProviderNetworks."""

        def __init__(self, **kwargs):
            """Init ProviderNetworks."""
            super().__init__(path="circuits/provider-networks/", **kwargs)

    class Providers(Base):
        """Providers."""

        def __init__(self, **kwargs):
            """Init Providers."""
            super().__init__(path="circuits/providers/", **kwargs)
            self._change_params = {
                "region": {"path": "dcim/regions/", "key": "name"},
                "site": {"path": "dcim/sites/", "key": "name"},
                "site_group": {"path": "dcim/site-groups/", "key": "name"},
            }

        # noinspection PyIncorrectDocstring
        def get(self, **kwargs) -> LDAny:
            """Get circuits/providers/ objects.

            WEB UI Filter parameters
            ------------------------

            :param q: Search. Substring of provider name.
            :type q: str or List[str]
            :example q: ["PROVIDER1", "PROVIDER2"]

            :param tag: Tag.
            :type tag: str or List[str]
            :example tag: ["alpha", "bravo"]

            :param region: Region.
            :type region: str or List[str]
            :example region: ["USA", "EU"]
            :param region_id: Region object ID.
            :type region_id: int or List[int]
            :example region_id: [1, 2]

            :param site_group: Site group.
            :type site_group: str or List[str]
            :example site_group: ["FRA", "FFL"]
            :param site_group_id: Site group object ID.
            :type site_group_id: int or List[int]
            :example site_group_id: [1, 2]

            :param site: Site name.
            :type site: str or List[str]
            :example site: ["FRA1", "FFL1"]
            :param site_id: Site object ID.
            :type site_id: int or List[int]
            :example site_id: [1, 2]

            Data Filter parameters
            ----------------------

            :param id: Object ID.
            :type id: int or List[int]
            :example id: [1, 2]

            :param name: Provider name.
            :type name: str or List[str]
            :example name: ["PROVIDER1", "PROVIDER2"]

            :param slug: Provider slug.
            :type slug: str or List[str]
            :example slug: ["provider1", "provider2"]

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)
