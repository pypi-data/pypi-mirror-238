"""Plugins Management."""

from vpnetbox.api.base import Base
from vpnetbox.types_ import DAny


class Plugins:  # pylint: disable=R0902,R0903
    """Plugins Management."""

    def __init__(self, **kwargs):
        """Init Extras."""
        self.installed_plugins = self.InstalledPlugins(**kwargs)

    class InstalledPlugins(Base):
        """InstalledPlugins."""

        def __init__(self, **kwargs):
            """Init InstalledPlugins."""
            super().__init__(path="plugins/installed-plugins/", **kwargs)

        def get(self, **kwargs) -> DAny:  # type: ignore
            """Get data."""
            _ = kwargs  # noqa
            return self._get_simple_data()
