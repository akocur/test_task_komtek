from django.contrib import admin

from services.terminology.models import Guide, GuideItem


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    """The class represents the Guide model in the admin interface."""

    list_display = ('name', 'short_name', 'version', 'start_date')
    list_filter = ['start_date']
    search_fields = ['name', 'short_name', 'version']


@admin.register(GuideItem)
class GuideItemAdmin(admin.ModelAdmin):
    """The class represents the GuideItem model in the admin interface."""

    list_display = ('code', 'value', 'guide')
