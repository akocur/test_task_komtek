from django.db import models
from django.utils import timezone


class Guide(models.Model):
    """Entity Guide."""

    name = models.CharField(
        max_length=200, verbose_name='Hаименование',  # noqa: WPS432
    )
    short_name = models.CharField(
        max_length=100,  # noqa: WPS432
        blank=True,
        verbose_name='Короткое наименование',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta(object):
        verbose_name_plural = 'Справочники'

    @property
    def current_version(self):
        """Return current version."""
        return self.get_version_on_date(timezone.now().date())

    def get_version_on_date(self, date):
        """Return guide version on the date."""
        return self.versions.filter(
            start_date__lte=date,
        ).order_by('-start_date').first()

    def get_guide_items(self, version=None):
        """Return guide items of the specified version.

        If version is None then return guide items of the current version.
        """
        if version is None:
            guid_version = self.current_version
            if guid_version is None:
                return []
        else:
            try:
                guid_version = self.versions.get(version=version)
            except GuideVersion.DoesNotExist:
                return []
        return guid_version.guide_items.all()

    def __str__(self):
        """Return  instanse representation."""
        return f'{self.id}, {self.name}'


class GuideItem(models.Model):
    """Entity GuideItem."""

    code = models.CharField(
        max_length=100,  # noqa: WPS432
        verbose_name='Код элемента',
    )
    value = models.CharField(  # noqa: WPS110
        max_length=200,  # noqa: WPS432
        verbose_name='Значение элемента',
    )

    class Meta(object):
        verbose_name_plural = 'Элементы справочников'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(code=''), name='non_empty_code',
            ),
            models.CheckConstraint(
                check=~models.Q(value=''), name='non_empty_value',
            ),
        ]

    def __str__(self):
        """Return  instanse representation."""
        return f'{self.id}, {self.value}'


class GuideVersion(models.Model):
    """Guide Versions."""

    guide = models.ForeignKey(
        Guide,
        models.CASCADE,
        related_name='versions',
        verbose_name='Справочник',
    )
    version = models.CharField(
        max_length=100,  # noqa: WPS432
        verbose_name='Версия',
    )
    start_date = models.DateField(
        verbose_name='Дата начала действия справочника',
    )
    guide_items = models.ManyToManyField(
        GuideItem, verbose_name='Элементы справочника',
    )

    class Meta(object):
        verbose_name_plural = 'Версии справочников'
        unique_together = ['guide', 'version']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(version=''), name='non_empty_version',
            ),
        ]

    def __str__(self):
        """Return  instanse representation."""
        return f'{self.version}, {self.guide}'
