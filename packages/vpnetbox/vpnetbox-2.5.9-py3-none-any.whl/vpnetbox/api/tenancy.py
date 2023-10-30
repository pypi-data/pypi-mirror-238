"""Tenancy Management."""

from vpnetbox.api.base import Base
from vpnetbox.types_ import LDAny


class Tenancy:  # pylint: disable=R0902,R0903
    """Tenancy Management."""

    def __init__(self, **kwargs):
        """Init Tenancy."""
        self.contact_assignments = self.ContactAssignments(**kwargs)
        self.contact_groups = self.ContactGroups(**kwargs)
        self.contact_roles = self.ContactRoles(**kwargs)
        self.contacts = self.Contacts(**kwargs)
        self.tenant_groups = self.TenantGroups(**kwargs)
        self.tenants = self.Tenants(**kwargs)

    class ContactAssignments(Base):
        """ContactAssignments."""

        def __init__(self, **kwargs):
            """Init ContactAssignments."""
            super().__init__(path="tenancy/contact-assignments/", **kwargs)

    class ContactGroups(Base):
        """ContactGroups."""

        def __init__(self, **kwargs):
            """Init ContactGroups."""
            super().__init__(path="tenancy/contact-groups/", **kwargs)

    class ContactRoles(Base):
        """ContactRoles."""

        def __init__(self, **kwargs):
            """Init ContactRoles."""
            super().__init__(path="tenancy/contact-roles/", **kwargs)

    class Contacts(Base):
        """Contacts."""

        def __init__(self, **kwargs):
            """Init Contacts."""
            super().__init__(path="tenancy/contacts/", **kwargs)

    class TenantGroups(Base):
        """TenantGroups."""

        def __init__(self, **kwargs):
            """Init TenantGroups."""
            super().__init__(path="tenancy/tenant-groups/", **kwargs)
            self._change_params = {
                "parent": {"query": "tenancy/tenant-groups/", "key": "name"},
            }

        # noinspection PyIncorrectDocstring
        def get(self, **kwargs) -> LDAny:
            """Get tenancy/tenant-groups/ objects.

            Each filter parameter can be either a single value or a list of values.
            The checked parameters are documented in the docstring,
            but not all filter parameters are documented.
            You can use any filter parameter that is available in the WEB UI.
            You can use some of the keys in the data object as filter parameters.

            WEB UI filter parameters
            ------------------------

            :param q: Search. Substring of tenant name.
            :type q: str or List[str]
            :example q: ["TENANT1", "TENANT2"]

            :param tag: Tag.
            :type tag: str or List[str]
            :example tag: ["alpha", "bravo"]

            :param group: Tenant group name.
            :type group: str or List[str]
            :example group: ["GROUP1", "GROUP2"]
            :param group_id: Tenant group object ID.
            :type group_id: int or List[int]
            :example group_id: [1, 2]

            :param parent: Tenant parent group name.
            :type parent: str or List[str]
            :example parent: ["TENANT GROUP1", "TENANT GROUP2"]
            :param parent_id: Tenant parent object ID.
            :type parent_id: int or List[int]
            :example parent_id: [1, 2]

            Data filter parameters
            ----------------------

            :param id: Object ID.
            :type id: int or List[int]
            :example id: [1, 2]

            :param name: Tenant group name.
            :type name: str or List[str]
            :example name: ["TENANT GROUP1", "TENANT GROUP2"]

            :param slug: Tenant group slug.
            :type slug: str or List[str]
            :example slug: ["tenant-group1", "tenant-group2"]

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)

    class Tenants(Base):
        """Tenants."""

        def __init__(self, **kwargs):
            """Init Tenants."""
            super().__init__(path="tenancy/tenants/", **kwargs)
            self._change_params = {
                "group": {"path": "tenancy/tenant-groups/", "key": "name"},
            }

        # noinspection PyIncorrectDocstring
        def get(self, **kwargs) -> LDAny:
            """Get tenancy/tenants/ objects.

            Each filter parameter can be either a single value or a list of values.
            The checked parameters are documented in the docstring,
            but not all filter parameters are documented.
            You can use any filter parameter that is available in the WEB UI.
            You can use some of the keys in the data object as filter parameters.

            WEB UI filter parameters
            ------------------------

            :param q: Search. Substring of tenant name.
            :type q: str or List[str]
            :example q: ["TENANT1", "TENANT2"]

            :param tag: Tag.
            :type tag: str or List[str]
            :example tag: ["alpha", "bravo"]

            :param group: Tenant group name.
            :type group: str or List[str]
            :example group: ["GROUP1", "GROUP2"]
            :param group_id: Tenant group object ID.
            :type group_id: int or List[int]
            :example group_id: [1, 2]

            Data filter parameters
            ----------------------

            :param id: Object ID.
            :type id: int or List[int]
            :example id: [1, 2]

            :param name: Tenant name.
            :type name: str or List[str]
            :example name: ["TENANT1", "TENANT2"]

            :param slug: Tenant slug.
            :type slug: str or List[str]
            :example slug: ["tenant1", "tenant1"]

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)
