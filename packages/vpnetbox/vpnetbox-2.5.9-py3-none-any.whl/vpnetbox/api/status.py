"""Status Management."""

from vpnetbox.api.base import Base
from vpnetbox.types_ import DAny


class Status(Base):
    """Status."""

    def __init__(self, **kwargs):
        """Init Status."""
        super().__init__(path="status/", **kwargs)

    def get(self, **kwargs) -> DAny:  # type: ignore
        """Get status.

        :return: Dictionary with status data.
        """
        _ = kwargs  # noqa
        return self._get_simple_data()
