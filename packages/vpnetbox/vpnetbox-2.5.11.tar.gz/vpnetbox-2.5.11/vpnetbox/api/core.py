"""Core Management."""

from vpnetbox.api.base import Base


class Core:  # pylint: disable=R0902,R0903
    """Core Management."""

    def __init__(self, **kwargs):
        """Init Core."""
        self.data_files = self.DataFiles(**kwargs)
        self.data_sources = self.DataSources(**kwargs)
        self.jobs = self.Jobs(**kwargs)

    class DataFiles(Base):
        """DataFiles."""

        def __init__(self, **kwargs):
            """Init DataFiles."""
            super().__init__(path="core/data-files/", **kwargs)

    class DataSources(Base):
        """DataSources."""

        def __init__(self, **kwargs):
            """Init DataSources."""
            super().__init__(path="core/data-sources/", **kwargs)

    class Jobs(Base):
        """Jobs."""

        def __init__(self, **kwargs):
            """Init Jobs."""
            super().__init__(path="core/jobs/", **kwargs)
