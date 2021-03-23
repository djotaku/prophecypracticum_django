from django.contrib import admin
from .models import Prophecy, ProphecyFeedback


# Register your models here.
@admin.register(Prophecy)
class ProphecyAdmin(admin.ModelAdmin):
    list_display = ('prophet', 'supplicant', 'publish', 'status')
    list_filter = ('prophet', 'supplicant', 'publish', 'status')
    raw_id_fields = ('prophet', 'supplicant',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(ProphecyFeedback)
class ProphecyFeedbackAdmin(admin.ModelAdmin):
    list_display = ('prophecy', 'publish', 'status')
    list_filter = ('prophecy', 'publish', 'status')
    raw_id_fields = ('prophecy',)
    ordering = ('status', 'publish')