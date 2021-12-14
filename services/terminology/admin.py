from django.contrib import admin

from services.terminology.models import Guide, GuideItem, GuideVersion


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    """The class represents the Guide model in the admin interface."""

    list_display = ('name', 'short_name')
    search_fields = ['name', 'short_name']


@admin.register(GuideVersion)
class GuideVersionAdmin(admin.ModelAdmin):
    """The class represents the GuideVersion model in the admin interface."""

    list_display = ('guide', 'version', 'start_date')


@admin.register(GuideItem)
class GuideItemAdmin(admin.ModelAdmin):
    """The class represents the GuideItem model in the admin interface."""

    list_display = ('code', 'value')
