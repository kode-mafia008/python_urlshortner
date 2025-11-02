from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics response"""
    total_urls = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    total_unique_visitors = serializers.IntegerField()
    clicks_today = serializers.IntegerField()
    clicks_this_week = serializers.IntegerField()
    top_urls = serializers.ListField(
        child=serializers.DictField()
    )


class TrendsSerializer(serializers.Serializer):
    """Serializer for trends response"""
    period_days = serializers.IntegerField()
    trends = serializers.ListField(
        child=serializers.DictField()
    )
