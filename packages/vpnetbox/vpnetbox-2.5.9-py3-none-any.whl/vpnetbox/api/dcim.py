"""Data Center Infrastructure Management."""

from vpnetbox.api.base import Base
from vpnetbox.types_ import LDAny


class Dcim:  # pylint: disable=R0902,R0903
    """Data Center Infrastructure Management."""

    def __init__(self, **kwargs):
        """Init Dcim."""
        self.cable_terminations = self.CableTerminations(**kwargs)
        self.cables = self.Cables(**kwargs)
        self.connected_device = self.ConnectedDevice(**kwargs)
        self.console_port_templates = self.ConsolePortTemplates(**kwargs)
        self.console_ports = self.ConsolePorts(**kwargs)
        self.console_server_port_templates = self.ConsoleServerPortTemplates(**kwargs)
        self.console_server_ports = self.ConsoleServerPorts(**kwargs)
        self.device_bay_templates = self.DeviceBayTemplates(**kwargs)
        self.device_bays = self.DeviceBays(**kwargs)
        self.device_roles = self.DeviceRoles(**kwargs)
        self.device_types = self.DeviceTypes(**kwargs)
        self.devices = self.Devices(**kwargs)
        self.front_port_templates = self.FrontPortTemplates(**kwargs)
        self.front_ports = self.FrontPorts(**kwargs)
        self.interface_templates = self.InterfaceTemplates(**kwargs)
        self.interfaces = self.Interfaces(**kwargs)
        self.inventory_item_roles = self.InventoryItemRoles(**kwargs)
        self.inventory_item_templates = self.InventoryItemTemplates(**kwargs)
        self.inventory_items = self.InventoryItems(**kwargs)
        self.locations = self.Locations(**kwargs)
        self.manufacturers = self.Manufacturers(**kwargs)
        self.module_bay_templates = self.ModuleBayTemplates(**kwargs)
        self.module_bays = self.ModuleBays(**kwargs)
        self.module_types = self.ModuleTypes(**kwargs)
        self.modules = self.Modules(**kwargs)
        self.platforms = self.Platforms(**kwargs)
        self.power_feeds = self.PowerFeeds(**kwargs)
        self.power_outlet_templates = self.PowerOutletTemplates(**kwargs)
        self.power_outlets = self.PowerOutlets(**kwargs)
        self.power_panels = self.PowerPanels(**kwargs)
        self.power_port_templates = self.PowerPortTemplates(**kwargs)
        self.power_ports = self.PowerPorts(**kwargs)
        self.rack_reservations = self.RackReservations(**kwargs)
        self.rack_roles = self.RackRoles(**kwargs)
        self.racks = self.Racks(**kwargs)
        self.rear_port_templates = self.RearPortTemplates(**kwargs)
        self.rear_ports = self.RearPorts(**kwargs)
        self.regions = self.Regions(**kwargs)
        self.site_groups = self.SiteGroups(**kwargs)
        self.sites = self.Sites(**kwargs)
        self.virtual_chassis = self.VirtualChassis(**kwargs)
        self.virtual_device_contexts = self.VirtualDeviceContexts(**kwargs)

    class CableTerminations(Base):
        """CableTerminations."""

        def __init__(self, **kwargs):
            """Init CableTerminations."""
            super().__init__(path="dcim/cable-terminations/", **kwargs)

    class Cables(Base):
        """Cables."""

        def __init__(self, **kwargs):
            """Init Cables."""
            super().__init__(path="dcim/cables/", **kwargs)

    class ConnectedDevice(Base):
        """ConnectedDevice."""

        def __init__(self, **kwargs):
            """Init ConnectedDevice."""
            super().__init__(path="dcim/connected-device/", **kwargs)

    class ConsolePortTemplates(Base):
        """ConsolePortTemplates."""

        def __init__(self, **kwargs):
            """Init ConsolePortTemplates."""
            super().__init__(path="dcim/console-port-templates/", **kwargs)

    class ConsolePorts(Base):
        """ConsolePorts."""

        def __init__(self, **kwargs):
            """Init ConsolePorts."""
            super().__init__(path="dcim/console-ports/", **kwargs)

    class ConsoleServerPortTemplates(Base):
        """ConsoleServerPortTemplates."""

        def __init__(self, **kwargs):
            """Init ConsoleServerPortTemplates."""
            super().__init__(path="dcim/console-server-port-templates/", **kwargs)

    class ConsoleServerPorts(Base):
        """ConsoleServerPorts."""

        def __init__(self, **kwargs):
            """Init ConsoleServerPorts."""
            super().__init__(path="dcim/console-server-ports/", **kwargs)

    class DeviceBayTemplates(Base):
        """DeviceBayTemplates."""

        def __init__(self, **kwargs):
            """Init DeviceBayTemplates."""
            super().__init__(path="dcim/device-bay-templates/", **kwargs)

    class DeviceBays(Base):
        """DeviceBays."""

        def __init__(self, **kwargs):
            """Init DeviceBays."""
            super().__init__(path="dcim/device-bays/", **kwargs)

    class DeviceRoles(Base):
        """DeviceRoles."""

        def __init__(self, **kwargs):
            """Init DeviceRoles."""
            super().__init__(path="dcim/device-roles/", **kwargs)

    class DeviceTypes(Base):
        """DeviceTypes."""

        def __init__(self, **kwargs):
            """Init DeviceTypes."""
            super().__init__(path="dcim/device-types/", **kwargs)
            self._sliced = "display_name"

    class Devices(Base):
        """Devices."""

        def __init__(self, **kwargs):
            """Init Devices."""
            super().__init__(path="dcim/devices/", **kwargs)
            self._sliced = "name"
            self._parallels.extend([
                "cf_sw_version",
                "has_primary_ip",
                "virtual_chassis_member",
            ])

        def get(self, **kwargs) -> LDAny:
            """Get dcim/devices/ objects.

            WEB UI filter parameters
            ------------------------

            Data filter parameters
            ----------------------

            :return: List of found objects.
            """
            _ = kwargs  # noqa
            return super().get(**kwargs)

    class FrontPortTemplates(Base):
        """FrontPortTemplates."""

        def __init__(self, **kwargs):
            """Init FrontPortTemplates."""
            super().__init__(path="dcim/front-port-templates/", **kwargs)

    class FrontPorts(Base):
        """FrontPorts."""

        def __init__(self, **kwargs):
            """Init FrontPorts."""
            super().__init__(path="dcim/front-ports/", **kwargs)

    class InterfaceTemplates(Base):
        """InterfaceTemplates."""

        def __init__(self, **kwargs):
            """Init InterfaceTemplates."""
            super().__init__(path="dcim/interface-templates/", **kwargs)

    class Interfaces(Base):
        """Interfaces."""

        def __init__(self, **kwargs):
            """Init Interfaces."""
            super().__init__(path="dcim/interfaces/", **kwargs)

    class InventoryItemRoles(Base):
        """InventoryItemRoles."""

        def __init__(self, **kwargs):
            """Init InventoryItemRoles."""
            super().__init__(path="dcim/inventory-item-roles/", **kwargs)

    class InventoryItemTemplates(Base):
        """InventoryItemTemplates."""

        def __init__(self, **kwargs):
            """Init InventoryItemTemplates."""
            super().__init__(path="dcim/inventory-item-templates/", **kwargs)

    class InventoryItems(Base):
        """InventoryItems."""

        def __init__(self, **kwargs):
            """Init InventoryItems."""
            super().__init__(path="dcim/inventory-items/", **kwargs)

    class Locations(Base):
        """Locations."""

        def __init__(self, **kwargs):
            """Init Locations."""
            super().__init__(path="dcim/locations/", **kwargs)

    class Manufacturers(Base):
        """Manufacturers."""

        def __init__(self, **kwargs):
            """Init Manufacturers."""
            super().__init__(path="dcim/manufacturers/", **kwargs)

    class ModuleBayTemplates(Base):
        """ModuleBayTemplates."""

        def __init__(self, **kwargs):
            """Init ModuleBayTemplates."""
            super().__init__(path="dcim/module-bay-templates/", **kwargs)

    class ModuleBays(Base):
        """ModuleBays."""

        def __init__(self, **kwargs):
            """Init ModuleBays."""
            super().__init__(path="dcim/module-bays/", **kwargs)

    class ModuleTypes(Base):
        """ModuleTypes."""

        def __init__(self, **kwargs):
            """Init ModuleTypes."""
            super().__init__(path="dcim/module-types/", **kwargs)

    class Modules(Base):
        """Modules."""

        def __init__(self, **kwargs):
            """Init Modules."""
            super().__init__(path="dcim/modules/", **kwargs)

    class Platforms(Base):
        """Platforms."""

        def __init__(self, **kwargs):
            """Init Platforms."""
            super().__init__(path="dcim/platforms/", **kwargs)

    class PowerFeeds(Base):
        """PowerFeeds."""

        def __init__(self, **kwargs):
            """Init PowerFeeds."""
            super().__init__(path="dcim/power-feeds/", **kwargs)

    class PowerOutletTemplates(Base):
        """PowerOutletTemplates."""

        def __init__(self, **kwargs):
            """Init PowerOutletTemplates."""
            super().__init__(path="dcim/power-outlet-templates/", **kwargs)

    class PowerOutlets(Base):
        """PowerOutlets."""

        def __init__(self, **kwargs):
            """Init PowerOutlets."""
            super().__init__(path="dcim/power-outlets/", **kwargs)

    class PowerPanels(Base):
        """PowerPanels."""

        def __init__(self, **kwargs):
            """Init PowerPanels."""
            super().__init__(path="dcim/power-panels/", **kwargs)

    class PowerPortTemplates(Base):
        """PowerPortTemplates."""

        def __init__(self, **kwargs):
            """Init PowerPortTemplates."""
            super().__init__(path="dcim/power-port-templates/", **kwargs)

    class PowerPorts(Base):
        """PowerPorts."""

        def __init__(self, **kwargs):
            """Init PowerPorts."""
            super().__init__(path="dcim/power-ports/", **kwargs)

    class RackReservations(Base):
        """RackReservations."""

        def __init__(self, **kwargs):
            """Init RackReservations."""
            super().__init__(path="dcim/rack-reservations/", **kwargs)

    class RackRoles(Base):
        """RackRoles."""

        def __init__(self, **kwargs):
            """Init RackRoles."""
            super().__init__(path="dcim/rack-roles/", **kwargs)

    class Racks(Base):
        """Racks."""

        def __init__(self, **kwargs):
            """Init Racks."""
            super().__init__(path="dcim/racks/", **kwargs)

    class RearPortTemplates(Base):
        """RearPortTemplates."""

        def __init__(self, **kwargs):
            """Init RearPortTemplates."""
            super().__init__(path="dcim/rear-port-templates/", **kwargs)

    class RearPorts(Base):
        """RearPorts."""

        def __init__(self, **kwargs):
            """Init RearPorts."""
            super().__init__(path="dcim/rear-ports/", **kwargs)

    class Regions(Base):
        """Regions."""

        def __init__(self, **kwargs):
            """Init Regions."""
            super().__init__(path="dcim/regions/", **kwargs)

    class SiteGroups(Base):
        """SiteGroups."""

        def __init__(self, **kwargs):
            """Init SiteGroups."""
            super().__init__(path="dcim/site-groups/", **kwargs)

    class Sites(Base):
        """Sites."""

        def __init__(self, **kwargs):
            """Init Sites."""
            super().__init__(path="dcim/sites/", **kwargs)

    class VirtualChassis(Base):
        """VirtualChassis."""

        def __init__(self, **kwargs):
            """Init VirtualChassis."""
            super().__init__(path="dcim/virtual-chassis/", **kwargs)

    class VirtualDeviceContexts(Base):
        """VirtualDeviceContexts."""

        def __init__(self, **kwargs):
            """Init VirtualDeviceContexts."""
            super().__init__(path="dcim/virtual-device-contexts/", **kwargs)
