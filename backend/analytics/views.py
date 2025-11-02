from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from shortener.models import URL, Click
from .models import DailyAnalytics


class DashboardStatsView(generics.GenericAPIView):
    """Get overall dashboard statistics"""
    
    def get(self, request):
        # Total URLs
        total_urls = URL.objects.filter(is_active=True).count()
        
        # Total clicks
        total_clicks = URL.objects.filter(is_active=True).aggregate(
            total=Sum('clicks')
        )['total'] or 0
        
        # Total unique visitors
        total_unique = URL.objects.filter(is_active=True).aggregate(
            total=Sum('unique_clicks')
        )['total'] or 0
        
        # Clicks today
        today = timezone.now().date()
        clicks_today = Click.objects.filter(
            clicked_at__date=today
        ).count()
        
        # Clicks this week
        week_ago = timezone.now() - timedelta(days=7)
        clicks_week = Click.objects.filter(
            clicked_at__gte=week_ago
        ).count()
        
        # Top URLs
        top_urls = URL.objects.filter(
            is_active=True
        ).order_by('-clicks')[:5].values(
            'short_code',
            'original_url',
            'clicks',
            'title'
        )
        
        return Response({
            'total_urls': total_urls,
            'total_clicks': total_clicks,
            'total_unique_visitors': total_unique,
            'clicks_today': clicks_today,
            'clicks_this_week': clicks_week,
            'top_urls': list(top_urls)
        })


class TrendsView(generics.GenericAPIView):
    """Get click trends over time"""
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)
        
        # Daily trends
        daily_trends = DailyAnalytics.objects.filter(
            date__gte=start_date
        ).values('date').annotate(
            total_clicks=Sum('clicks'),
            total_unique=Sum('unique_visitors')
        ).order_by('date')
        
        return Response({
            'period_days': days,
            'trends': list(daily_trends)
        })
