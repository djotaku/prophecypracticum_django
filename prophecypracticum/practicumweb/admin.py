from django.contrib import admin
from .models import Prophecy, ProphecyFeedback, WeeklyLink


# Register your models here.
@admin.register(Prophecy)
class ProphecyAdmin(admin.ModelAdmin):
    list_display = ('prophet', 'supplicant', 'publish', 'status')
    list_filter = ( 'week_name', 'prophet', 'supplicant', 'publish', 'status')
    raw_id_fields = ('prophet', 'supplicant',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(ProphecyFeedback)
class ProphecyFeedbackAdmin(admin.ModelAdmin):
    list_display = ('prophecy', 'publish', 'status')
    list_filter = ('week_name', 'prophecy', 'publish', 'status')
    raw_id_fields = ('prophecy',)
    ordering = ('status', 'publish')


@admin.register(WeeklyLink)
class WeeklyLinkAdmin(admin.ModelAdmin):
    date_hierarchy = 'sunday_date'
    list_display = ('prophet', 'view_user_first_name', 'view_user_last_name', 'supplicant', 'sunday_date',
                    'week_name')
    list_filter = ('week_name', 'prophet', 'supplicant', 'sunday_date')
    raw_id_fields = ('prophet', 'supplicant',)
    ordering = ('sunday_date',)

    def view_user_first_name(self, obj):
        return obj.prophet.first_name

    def view_user_last_name(self, obj):
        return obj.prophet.last_name
