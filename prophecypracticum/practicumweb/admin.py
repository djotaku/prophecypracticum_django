from django.contrib import admin
from .models import Prophecy, ProphecyFeedback, WeeklyLink, PracticumNames


# Register your models here.
@admin.register(Prophecy)
class ProphecyAdmin(admin.ModelAdmin):
    list_display = ('prophet', 'prophet_name', "supplicant_name", 'supplicant', 'publish', 'status')
    list_filter = ('week_name', 'prophet', 'supplicant', 'publish', 'status')
    raw_id_fields = ('prophet', 'supplicant',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    def prophet_name(self, obj):
        return f"{obj.prophet.first_name} {obj.prophet.last_name}"

    def supplicant_name(self, obj):
        return f"{obj.supplicant.first_name} {obj.supplicant.last_name}"


@admin.register(ProphecyFeedback)
class ProphecyFeedbackAdmin(admin.ModelAdmin):
    list_display = ('prophecy', 'prophet_name', "supplicant_name", 'publish', 'status')
    list_filter = ('week_name', 'prophecy', 'publish', 'status')
    raw_id_fields = ('prophecy',)
    ordering = ('status', 'publish')

    def prophet_name(self, obj):
        return f"{obj.prophet.first_name} {obj.prophet.last_name}"

    def supplicant_name(self, obj):
        return f"{obj.supplicant.first_name} {obj.supplicant.last_name}"


@admin.register(WeeklyLink)
class WeeklyLinkAdmin(admin.ModelAdmin):
    date_hierarchy = 'sunday_date'
    list_display = ('prophet', 'prophet_name', 'supplicant', 'supplicant_name', 'sunday_date',
                    'week_name',)
    list_filter = ('week_name', 'prophet', 'supplicant', 'sunday_date')
    raw_id_fields = ('prophet', 'supplicant',)
    ordering = ('sunday_date',)

    def prophet_name(self, obj):
        return f"{obj.prophet.first_name} {obj.prophet.last_name}"

    def supplicant_name(self, obj):
        return f"{obj.supplicant.first_name} {obj.supplicant.last_name}"


@admin.register(PracticumNames)
class PracticumNamesAdmin(admin.ModelAdmin):
    list_display = ('week_name',)
