from django.contrib import admin
from django.utils.html import format_html
from .models import URL, Click


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ['short_code', 'original_url_truncated', 'clicks', 'is_active', 'created_at']
    list_filter = ['is_active', 'custom_code', 'created_at']
    search_fields = ['short_code', 'original_url', 'title']
    readonly_fields = ['short_code', 'clicks', 'unique_clicks', 'created_at', 'updated_at']
    
    def original_url_truncated(self, obj):
        return obj.original_url[:50] + '...' if len(obj.original_url) > 50 else obj.original_url


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip_address', 'device_type', 'browser', 'clicked_at']
    list_filter = ['device_type', 'browser', 'clicked_at']
    search_fields = ['ip_address', 'referer']
    readonly_fields = ['url', 'clicked_at']
