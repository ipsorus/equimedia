from django.contrib import admin

from event.models import Event, Tournament, EventDocument, TournamentDocument, StageDocument, Stage, EventType, \
    ContestType, Discipline


class StageDocumentsInline(admin.TabularInline):
    extra = 0
    model = StageDocument


class StageAdmin(admin.ModelAdmin):
    inlines = [StageDocumentsInline]


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


class TournamentDocumentsInline(admin.StackedInline):
    extra = 0
    model = TournamentDocument


class StageInline(admin.StackedInline):
    extra = 0
    model = Stage


class TournamentAdmin(admin.ModelAdmin):
    inlines = [StageInline, TournamentDocumentsInline]


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(ContestType, ContestTypeAdmin)

