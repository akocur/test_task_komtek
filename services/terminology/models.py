from django.db import models


class Guide(models.Model):
    """Entity Guide."""

    name = models.CharField(max_length=200)  # noqa: WPS432
    short_name = models.CharField(max_length=100, blank=True)  # noqa: WPS432
    description = models.TextField(blank=True)
    version = models.CharField(max_length=100)  # noqa: WPS432
    start_date = models.DateField()

    class Meta(object):
        ordering = ['name', 'start_date', 'id']
        unique_together = ['name', 'version']

    def __str__(self):
        """Display the class as a 'name, version' string instead 'id'."""
        return f'{self.name}, {self.version}'


class GuideItem(models.Model):
    """Entity GuideItem."""

    guide = models.ForeignKey('Guide', on_delete=models.CASCADE)
    code = models.CharField(max_length=100)  # noqa: WPS432
    value = models.CharField(max_length=200)  # noqa: WPS432, WPS110

    class Meta(object):
        ordering = ['code', 'guide', 'id']
