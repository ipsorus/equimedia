from django.contrib import admin
from django.db import ProgrammingError

from event.models import Event, Tournament, EventDocument, TournamentDocument, StageDocument, Stage, EventType, \
    ContestType, Discipline, EventSettings, BannerEventSideBar1, BannerEventSideBar2, StageCloseDocument, \
    TournamentCloseDocument


class StageDocumentsInline(admin.TabularInline):
    extra = 0
    model = StageDocument


class StageCloseDocumentInline(admin.TabularInline):
    extra = 0
    model = StageCloseDocument


class StageAdmin(admin.ModelAdmin):
    inlines = [StageDocumentsInline, StageCloseDocumentInline]


class EventDocumentsInline(admin.TabularInline):
    extra = 0
    model = EventDocument


class DisciplineAdmin(admin.ModelAdmin):
    model = Discipline


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType


class ContestTypeAdmin(admin.ModelAdmin):
    model = ContestType


class EventAdmin(admin.ModelAdmin):
    inlines = [EventDocumentsInline]


class TournamentCloseDocumentInline(admin.TabularInline):
    extra = 0
    model = TournamentCloseDocument


class TournamentDocumentsInline(admin.StackedInline):
    extra = 0
    model = TournamentDocument


class StageInline(admin.StackedInline):
    extra = 0
    model = Stage


class TournamentAdmin(admin.ModelAdmin):
    inlines = [StageInline, TournamentDocumentsInline, TournamentCloseDocumentInline]


class EventSettingsAdmin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            EventSettings.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False


class BannerEventSideBar1Admin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            BannerEventSideBar1.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False


class BannerEventSideBar2Admin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            BannerEventSideBar2.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(BannerEventSideBar1, BannerEventSideBar1Admin)
admin.site.register(BannerEventSideBar2, BannerEventSideBar2Admin)
admin.site.register(EventSettings, EventSettingsAdmin)

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(ContestType, ContestTypeAdmin)

