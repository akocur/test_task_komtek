from django.db import models
from django.utils import timezone


class Guide(models.Model):
    """Entity Guide."""

    name = models.CharField(max_length=200)  # noqa: WPS432
    short_name = models.CharField(max_length=100, blank=True)  # noqa: WPS432
    description = models.TextField(blank=True)

    @property
    def current_version(self):
        """Return current version."""
        return self.versions.filter(
            start_date__lte=timezone.now().date(),
        ).order_by('-start_date').first()

    def get_guide_items(self, version=None):
        """Return guide items of the specified version.

        If version is None then return guide items of the current version.
        """
        guid_version = self.versions.get(version=version)
        if version is None:
            guid_version = self.current_version
        return guid_version.guide_items.all()

    def __str__(self):
        """Return  instanse representation."""
        return f'{self.id}, {self.name}'


class GuideItem(models.Model):
    """Entity GuideItem."""

    code = models.CharField(max_length=100)  # noqa: WPS432
    value = models.CharField(max_length=200)  # noqa: WPS432, WPS110

    def __str__(self):
        """Return  instanse representation."""
        return f'{self.id}, {self.value}'


class GuideVersion(models.Model):
    """Guide Versions."""

    guide = models.ForeignKey(Guide, models.CASCADE, related_name='versions')
    version = models.CharField(max_length=100)  # noqa: WPS432
    start_date = models.DateField()
    guide_items = models.ManyToManyField(GuideItem)

    class Meta(object):
        unique_together = ['guide', 'version']

    def __str__(self):
        """Return  instanse representation."""
        return f'{self.version}, {self.guide}'
