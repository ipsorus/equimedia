from django.contrib import admin
from django.db import ProgrammingError

from podcast.models import Video, VideoSettings


class VideoAdmin(admin.ModelAdmin):
    model = Video


class VideoSettingsAdmin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            VideoSettings.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(VideoSettings, VideoSettingsAdmin)
admin.site.register(Video, VideoAdmin)
