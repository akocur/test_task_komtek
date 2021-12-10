from django.db import models
from django.utils import timezone


class Guide(models.Model):
    """Entity Guide."""

    name = models.CharField(max_length=200)  # noqa: WPS432
    short_name = models.CharField(max_length=100, blank=True)  # noqa: WPS432
    description = models.TextField(blank=True)
    version = models.CharField(max_length=100)  # noqa: WPS432
    start_date = models.DateField()

    @classmethod
    def current_version(cls, name):
        """Return current version by name."""
        return cls.objects.filter(
            name=name, start_date__lte=timezone.now().date(),
        ).order_by('-start_date').first()

    class Meta(object):
        ordering = ['name', 'start_date', 'id']
        unique_together = ['name', 'version']

    def __str__(self):
        """Display the class as a 'name, version' string instead 'id'."""
        return f'{self.name}, {self.version}'


class GuideItem(models.Model):
    """Entity GuideItem."""

    guide = models.ForeignKey(
        Guide,
        on_delete=models.CASCADE,
        related_name='items',
    )
    code = models.CharField(max_length=100)  # noqa: WPS432
    value = models.CharField(max_length=200)  # noqa: WPS432, WPS110

    class Meta(object):
        ordering = ['code', 'guide', 'id']
