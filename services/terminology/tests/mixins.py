import datetime

from django.utils import timezone

from services.terminology.models import Guide, GuideItem


class GuideMixin(object):
    """Provide methods for working with guide."""

    default_guide_name = 'guide1'
    default_guide_short_name = 'g1'
    default_guide_description = 'description1'

    def create_guide(self, name, short_name='', description=''):
        """Create guide."""
        return Guide.objects.create(
            name=name, short_name=short_name, description=description,
        )

    def get_guide(self, **kwargs):
        """Get guide."""
        return Guide.objects.get(**kwargs)


class GuideVersionMixin(object):
    """Provide methods for working with guide version."""

    last_version_name = 'last'
    current_version_name = 'current'
    future_version_name = 'future'

    def create_version(self, guide, version, start_date, guide_items=None):
        """Create guide version."""
        if guide_items is None:
            guide_items = []
        guide_version = guide.versions.create(
            version=version, start_date=start_date,
        )
        if guide_items:
            guide_version.guide_items.add(guide_items)
        return guide_version

    def create_last_version(self, guide, guide_items=None):
        """Create last guide version."""
        today = timezone.now().date()
        last_date = today - datetime.timedelta(days=30)  # noqa: WPS432
        return self.create_version(
            guide, self.last_version_name, last_date, guide_items=guide_items,
        )

    def create_current_version(self, guide, guide_items=None):
        """Create last guide version."""
        today = timezone.now().date()
        return self.create_version(
            guide, self.current_version_name, today, guide_items=guide_items,
        )

    def create_future_version(self, guide, guide_items=None):
        """Create last guide version."""
        today = timezone.now().date()
        future_date = today + datetime.timedelta(days=30)  # noqa: WPS432
        return self.create_version(
            guide,
            self.future_version_name,
            future_date,
            guide_items=guide_items,
        )


class GuideItemMixin(object):
    """Provide methods for working with guide item."""

    def create_guide_item(self, code, value):  # noqa: WPS110
        """Create guide item."""
        return GuideItem.objects.create(code=code, value=value)
