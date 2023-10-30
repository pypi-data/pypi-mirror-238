"""Users Management."""

from vpnetbox.api.base import Base
from vpnetbox.types_ import DAny


class UsersM:  # pylint: disable=R0902,R0903
    """Users Management."""

    def __init__(self, **kwargs):
        """Init Users."""
        self.config = self.Config(**kwargs)
        self.groups = self.Groups(**kwargs)
        self.permissions = self.Permissions(**kwargs)
        self.tokens = self.Tokens(**kwargs)
        self.users = self.Users(**kwargs)

    class Config(Base):
        """Config."""

        def __init__(self, **kwargs):
            """Init Config."""
            super().__init__(path="users/config/", **kwargs)

        def get(self, **kwargs) -> DAny:  # type: ignore
            """Get data."""
            _ = kwargs  # noqa
            return self._get_simple_data()

    class Groups(Base):
        """Groups."""

        def __init__(self, **kwargs):
            """Init Groups."""
            super().__init__(path="users/groups/", **kwargs)

        def get(self, **kwargs) -> DAny:  # type: ignore
            """Get data."""
            _ = kwargs  # noqa
            return self._get_simple_data()

    class Permissions(Base):
        """Permissions."""

        def __init__(self, **kwargs):
            """Init Permissions."""
            super().__init__(path="users/permissions/", **kwargs)

        def get(self, **kwargs) -> DAny:  # type: ignore
            """Get data."""
            _ = kwargs  # noqa
            return self._get_simple_data()

    class Tokens(Base):
        """Tokens."""

        def __init__(self, **kwargs):
            """Init Tokens."""
            super().__init__(path="users/tokens/", **kwargs)

        def get(self, **kwargs) -> DAny:  # type: ignore
            """Get data."""
            _ = kwargs  # noqa
            return self._get_simple_data()

    class Users(Base):
        """Users."""

        def __init__(self, **kwargs):
            """Init Users."""
            super().__init__(path="users/users/", **kwargs)

        def get(self, **kwargs) -> DAny:  # type: ignore
            """Get data."""
            _ = kwargs  # noqa
            return self._get_simple_data()
