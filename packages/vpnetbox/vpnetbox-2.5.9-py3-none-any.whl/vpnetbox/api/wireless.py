"""Wireless Management."""

from vpnetbox.api.base import Base


class Wireless:  # pylint: disable=R0902,R0903
    """Wireless Management."""

    def __init__(self, **kwargs):
        """Init Wireless."""
        self.wireless_lan_groups = self.WirelessLanGroups(**kwargs)
        self.wireless_lans = self.WirelessLans(**kwargs)
        self.wireless_links = self.WirelessLinks(**kwargs)

    class WirelessLanGroups(Base):
        """WirelessLanGroups."""

        def __init__(self, **kwargs):
            """Init WirelessLanGroups."""
            super().__init__(path="wireless/wireless-lan-groups/", **kwargs)

    class WirelessLans(Base):
        """WirelessLans."""

        def __init__(self, **kwargs):
            """Init WirelessLans."""
            super().__init__(path="wireless/wireless-lans/", **kwargs)

    class WirelessLinks(Base):
        """WirelessLinks."""

        def __init__(self, **kwargs):
            """Init WirelessLinks."""
            super().__init__(path="wireless/wireless-links/", **kwargs)
