"""NbApi, Python wrapper of Netbox REST API.

Requests data from the Netbox REST API using filter parameters identical
to those in the web interface filter form.

Key features:

* Retries the request multiple times if the Netbox API responds with a ServerError 500 or timed-out.
    This is useful for scheduled scripts in cron jobs, when the Netbox server is overloaded and
    unable to process all the requests.
* Slices the query to multiple requests if the URL length exceeds 4000 characters (due to a long
    list of GET parameters). This is useful for retrieving a long list of addresses.
* Replaces an error-400 response with an empty result. For example, when querying addresses by tag,
    if there are no address objects with this tag in Netbox, the default Netbox API response is
    error-400. This package logs a warning and returns an ok-200 response with an empty list.
"""

from __future__ import annotations

from vpnetbox.api.circuits import CircuitsM
from vpnetbox.api.core import Core
from vpnetbox.api.dcim import Dcim
from vpnetbox.api.extras import Extras
from vpnetbox.api.ipam import Ipam
from vpnetbox.api.plugins import Plugins
from vpnetbox.api.status import Status
from vpnetbox.api.tenancy import Tenancy
from vpnetbox.api.users import UsersM
from vpnetbox.api.virtualization import Virtualization
from vpnetbox.api.wireless import Wireless


class NbApi:  # pylint: disable=R0902
    """NbApi, Python wrapper of Netbox REST API.

    Requests data from the Netbox REST API using filter parameters identical
    to those in the web interface filter form.
    """

    def __init__(self, **kwargs):  # pylint: disable=R0915
        """Init NbApi.

        :param host: Netbox host name.
        :type host: str

        :param token: Netbox token.
        :type token: str

        :param scheme: Access method: https or http. Default "https".
        :type scheme: str

        :param verify: Transport Layer Security. True - A TLS certificate required,
        False - Requests will accept any TLS certificate.
        :type verify: bool

        :param limit: Split the query to multiple requests if the response exceeds the limit.
            Default 1000.
        :type limit: int

        :param threads: Threads count. Default 1, loop mode.
        :type threads: int

        :param interval: Wait this time between requests (seconds).
            Default 0. Useful for request speed shaping.
        :type interval: int

        :param max_items: Stop the request if received items reach this value.
            Default unlimited. Useful if you need many objects but not all.
        :type max_items: int

        :param timeout: Request timeout (seconds). Default 60.
        :type timeout: float

        :param max_retries: Retry the request multiple times if it receives a 500 error
            or timed-out. Default 3.
        :type max_retries: int

        :param sleep: Interval before the next retry after receiving a 500 error (seconds).
            Default 10.
        :type sleep: float

        :param url_max_len: Split the query to multiple requests if the URL length exceeds
            this value. Default ~3900.
        :type url_max_len: int
        """
        # circuits
        self.circuits = CircuitsM(**kwargs)
        self.circuit_terminations = self.circuits.circuit_terminations
        self.circuit_types = self.circuits.circuit_types
        self.circuits_ = self.circuits.circuits  # overlap with CircuitsM
        self.provider_networks = self.circuits.provider_networks
        self.providers = self.circuits.providers
        # core
        self.core = Core(**kwargs)
        self.data_files = self.core.data_files
        self.data_sources = self.core.data_sources
        self.jobs = self.core.jobs
        # dcim
        self.dcim = Dcim(**kwargs)
        self.cable_terminations = self.dcim.cable_terminations
        self.cables = self.dcim.cables
        self.console_port_templates = self.dcim.console_port_templates
        self.console_ports = self.dcim.console_ports
        self.console_server_port_templates = self.dcim.console_server_port_templates
        self.console_server_ports = self.dcim.console_server_ports
        self.device_bay_templates = self.dcim.device_bay_templates
        self.device_bays = self.dcim.device_bays
        self.device_roles = self.dcim.device_roles
        self.device_types = self.dcim.device_types
        self.devices = self.dcim.devices
        self.front_port_templates = self.dcim.front_port_templates
        self.front_ports = self.dcim.front_ports
        self.interface_templates = self.dcim.interface_templates
        self.interfaces = self.dcim.interfaces  # overlap with virtualization.interfaces
        self.inventory_item_roles = self.dcim.inventory_item_roles
        self.inventory_item_templates = self.dcim.inventory_item_templates
        self.inventory_items = self.dcim.inventory_items
        self.locations = self.dcim.locations
        self.manufacturers = self.dcim.manufacturers
        self.module_bay_templates = self.dcim.module_bay_templates
        self.module_bays = self.dcim.module_bays
        self.module_types = self.dcim.module_types
        self.modules = self.dcim.modules
        self.platforms = self.dcim.platforms
        self.power_feeds = self.dcim.power_feeds
        self.power_outlet_templates = self.dcim.power_outlet_templates
        self.power_outlets = self.dcim.power_outlets
        self.power_panels = self.dcim.power_panels
        self.power_port_templates = self.dcim.power_port_templates
        self.power_ports = self.dcim.power_ports
        self.rack_reservations = self.dcim.rack_reservations
        self.rack_roles = self.dcim.rack_roles
        self.racks = self.dcim.racks
        self.rear_port_templates = self.dcim.rear_port_templates
        self.rear_ports = self.dcim.rear_ports
        self.regions = self.dcim.regions
        self.site_groups = self.dcim.site_groups
        self.sites = self.dcim.sites
        self.virtual_chassis = self.dcim.virtual_chassis
        self.virtual_device_contexts = self.dcim.virtual_device_contexts
        # extras
        self.extras = Extras(**kwargs)
        self.bookmarks = self.extras.bookmarks
        self.config_contexts = self.extras.config_contexts
        self.config_templates = self.extras.config_templates
        self.content_types = self.extras.content_types
        self.custom_field_choice_sets = self.extras.custom_field_choice_sets
        self.custom_fields = self.extras.custom_fields
        self.custom_links = self.extras.custom_links
        self.export_templates = self.extras.export_templates
        self.image_attachments = self.extras.image_attachments
        self.journal_entries = self.extras.journal_entries
        self.object_changes = self.extras.object_changes
        self.reports = self.extras.reports
        self.saved_filters = self.extras.saved_filters
        self.scripts = self.extras.scripts
        self.tags = self.extras.tags
        self.webhooks = self.extras.webhooks
        # ipam
        self.ipam = Ipam(**kwargs)
        self.aggregates = self.ipam.aggregates
        self.asn_ranges = self.ipam.asn_ranges
        self.asns = self.ipam.asns
        self.fhrp_group_assignments = self.ipam.fhrp_group_assignments
        self.fhrp_groups = self.ipam.fhrp_groups
        self.ip_addresses = self.ipam.ip_addresses
        self.ip_ranges = self.ipam.ip_ranges
        self.l2vpn_terminations = self.ipam.l2vpn_terminations
        self.l2vpns = self.ipam.l2vpns
        self.prefixes = self.ipam.prefixes
        self.rirs = self.ipam.rirs
        self.roles = self.ipam.roles
        self.route_targets = self.ipam.route_targets
        self.service_templates = self.ipam.service_templates
        self.services = self.ipam.services
        self.vlan_groups = self.ipam.vlan_groups
        self.vlans = self.ipam.vlans
        self.vrfs = self.ipam.vrfs
        # plugins
        self.plugins = Plugins(**kwargs)
        # status
        self.status = Status(**kwargs)
        # tenancy
        self.tenancy = Tenancy(**kwargs)
        self.contact_assignments = self.tenancy.contact_assignments
        self.contact_groups = self.tenancy.contact_groups
        self.contact_roles = self.tenancy.contact_roles
        self.contacts = self.tenancy.contacts
        self.tenant_groups = self.tenancy.tenant_groups
        self.tenants = self.tenancy.tenants
        # users
        self.users = UsersM(**kwargs)
        # virtualization
        self.virtualization = Virtualization(**kwargs)
        self.cluster_groups = self.virtualization.cluster_groups
        self.cluster_types = self.virtualization.cluster_types
        self.clusters = self.virtualization.clusters
        self.interfaces_ = self.virtualization.interfaces  # overlap with dcim.interfaces
        self.virtual_machines = self.virtualization.virtual_machines
        # wireless
        self.wireless = Wireless(**kwargs)
        self.wireless_lan_groups = self.wireless.wireless_lan_groups
        self.wireless_lans = self.wireless.wireless_lans
        self.wireless_links = self.wireless.wireless_links

        # self.version = self.objects.version  # todo via status

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        return f"<{name}: {self.host}>"

    @property
    def host(self) -> str:
        """Netbox host name."""
        return self.ipam.aggregates.host

    # =========================== method =============================
    def default_active(self) -> None:
        """Set default filter parameters for all objects.

        This is useful when you only need to work with active IPv4 objects.
        """
        # ipam
        self.ipam.aggregates.default = {"family": 4}
        self.ipam.ip_addresses.default = {"family": 4, "status": "active"}
        self.ip_ranges.default = {"family": 4, "status": ["active"]}
        self.ipam.prefixes.default = {"family": 4, "status": ["active", "container"]}
        self.ipam.vlans.default = {"status": "active"}
        # dcim
        self.dcim.devices.default = {"has_primary_ip": True, "status": "active"}
        self.dcim.sites.default = {"status": "active"}
        # circuits
        self.circuits.circuits.default = {"status": "active"}
