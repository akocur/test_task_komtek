from django.db import models


class Guide(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=100)
    start_date = models.DateField()

    class Meta(object):
        ordering = ['name', 'start_date', 'id']
        unique_together = ['name', 'version']

    def __str__(self):
        return f'{self.name}, {self.version}'


class GuideItem(models.Model):
    guide = models.ForeignKey('Guide', on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    class Meta(object):
        ordering = ['code', 'guide', 'id']
