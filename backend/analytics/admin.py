from django.contrib import admin
from .models import DailyAnalytics


@admin.register(DailyAnalytics)
class DailyAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['url', 'date', 'clicks', 'unique_visitors']
    list_filter = ['date']
    search_fields = ['url__short_code']
    readonly_fields = ['url', 'date', 'clicks', 'unique_visitors']
