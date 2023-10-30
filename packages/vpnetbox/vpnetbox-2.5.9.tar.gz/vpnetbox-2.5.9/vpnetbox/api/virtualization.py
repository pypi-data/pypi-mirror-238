"""Virtualization Management."""

from vpnetbox.api.base import Base


class Virtualization:  # pylint: disable=R0902,R0903
    """Virtualization Management."""

    def __init__(self, **kwargs):
        """Init Virtualization."""
        self.cluster_groups = self.ClusterGroups(**kwargs)
        self.cluster_types = self.ClusterTypes(**kwargs)
        self.clusters = self.Clusters(**kwargs)
        self.interfaces = self.Interfaces(**kwargs)
        self.virtual_machines = self.VirtualMachines(**kwargs)

    class ClusterGroups(Base):
        """ClusterGroups."""

        def __init__(self, **kwargs):
            """Init ClusterGroups."""
            super().__init__(path="virtualization/cluster-groups/", **kwargs)

    class ClusterTypes(Base):
        """ClusterTypes."""

        def __init__(self, **kwargs):
            """Init ClusterTypes."""
            super().__init__(path="virtualization/cluster-types/", **kwargs)

    class Clusters(Base):
        """Clusters."""

        def __init__(self, **kwargs):
            """Init Clusters."""
            super().__init__(path="virtualization/clusters/", **kwargs)

    class Interfaces(Base):
        """Interfaces."""

        def __init__(self, **kwargs):
            """Init Interfaces."""
            super().__init__(path="virtualization/interfaces/", **kwargs)

    class VirtualMachines(Base):
        """VirtualMachines."""

        def __init__(self, **kwargs):
            """Init VirtualMachines."""
            super().__init__(path="virtualization/virtual-machines/", **kwargs)
