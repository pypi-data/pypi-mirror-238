"""Extras Management."""

from vpnetbox.api.base import Base


class Extras:  # pylint: disable=R0902,R0903
    """Extras Management."""

    def __init__(self, **kwargs):
        """Init Extras."""
        self.bookmarks = self.Bookmarks(**kwargs)
        self.config_contexts = self.ConfigContexts(**kwargs)
        self.config_templates = self.ConfigTemplates(**kwargs)
        self.content_types = self.ContentTypes(**kwargs)
        self.custom_field_choice_sets = self.CustomFieldChoiceSets(**kwargs)
        self.custom_fields = self.CustomFields(**kwargs)
        self.custom_links = self.CustomLinks(**kwargs)
        self.export_templates = self.ExportTemplates(**kwargs)
        self.image_attachments = self.ImageAttachments(**kwargs)
        self.journal_entries = self.JournalEntries(**kwargs)
        self.object_changes = self.ObjectChanges(**kwargs)
        self.reports = self.Reports(**kwargs)
        self.saved_filters = self.SavedFilters(**kwargs)
        self.scripts = self.Scripts(**kwargs)
        self.tags = self.Tags(**kwargs)
        self.webhooks = self.Webhooks(**kwargs)

    class Bookmarks(Base):
        """Bookmarks."""

        def __init__(self, **kwargs):
            """Init Bookmarks."""
            super().__init__(path="extras/bookmarks/", **kwargs)

    class ConfigContexts(Base):
        """ConfigContexts."""

        def __init__(self, **kwargs):
            """Init ConfigContexts."""
            super().__init__(path="extras/config-contexts/", **kwargs)

    class ConfigTemplates(Base):
        """ConfigTemplates."""

        def __init__(self, **kwargs):
            """Init ConfigTemplates."""
            super().__init__(path="extras/config-templates/", **kwargs)

    class ContentTypes(Base):
        """ContentTypes."""

        def __init__(self, **kwargs):
            """Init ContentTypes."""
            super().__init__(path="extras/content-types/", **kwargs)

    class CustomFieldChoiceSets(Base):
        """CustomFieldChoiceSets."""

        def __init__(self, **kwargs):
            """Init CustomFieldChoiceSets."""
            super().__init__(path="extras/custom-field-choice-sets/", **kwargs)

    class CustomFields(Base):
        """CustomFields."""

        def __init__(self, **kwargs):
            """Init CustomFields."""
            super().__init__(path="extras/custom-fields/", **kwargs)

    class CustomLinks(Base):
        """CustomLinks."""

        def __init__(self, **kwargs):
            """Init CustomLinks."""
            super().__init__(path="extras/custom-links/", **kwargs)

    class ExportTemplates(Base):
        """ExportTemplates."""

        def __init__(self, **kwargs):
            """Init ExportTemplates."""
            super().__init__(path="extras/export-templates/", **kwargs)

    class ImageAttachments(Base):
        """ImageAttachments."""

        def __init__(self, **kwargs):
            """Init ImageAttachments."""
            super().__init__(path="extras/image-attachments/", **kwargs)

    class JournalEntries(Base):
        """JournalEntries."""

        def __init__(self, **kwargs):
            """Init JournalEntries."""
            super().__init__(path="extras/journal-entries/", **kwargs)

    class ObjectChanges(Base):
        """ObjectChanges."""

        def __init__(self, **kwargs):
            """Init ObjectChanges."""
            super().__init__(path="extras/object-changes/", **kwargs)

    class Reports(Base):
        """Reports."""

        def __init__(self, **kwargs):
            """Init Reports."""
            super().__init__(path="extras/reports/", **kwargs)

    class SavedFilters(Base):
        """SavedFilters."""

        def __init__(self, **kwargs):
            """Init SavedFilters."""
            super().__init__(path="extras/saved-filters/", **kwargs)

    class Scripts(Base):
        """Scripts."""

        def __init__(self, **kwargs):
            """Init Scripts."""
            super().__init__(path="extras/scripts/", **kwargs)

    class Tags(Base):
        """Tags."""

        def __init__(self, **kwargs):
            """Init Tags."""
            super().__init__(path="extras/tags/", **kwargs)

    class Webhooks(Base):
        """Webhooks."""

        def __init__(self, **kwargs):
            """Init Webhooks."""
            super().__init__(path="extras/webhooks/", **kwargs)
