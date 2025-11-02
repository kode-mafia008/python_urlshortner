from celery import shared_task
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def aggregate_analytics():
    """Aggregate click data into daily analytics"""
    try:
        from shortener.models import Click
        from .models import DailyAnalytics
        
        yesterday = timezone.now().date() - timedelta(days=1)
        
        # Aggregate clicks by URL for yesterday
        daily_stats = Click.objects.filter(
            clicked_at__date=yesterday
        ).values('url').annotate(
            clicks=Count('id'),
            unique_visitors=Count('session_id', distinct=True)
        )
        
        # Update or create daily analytics records
        for stat in daily_stats:
            DailyAnalytics.objects.update_or_create(
                url_id=stat['url'],
                date=yesterday,
                defaults={
                    'clicks': stat['clicks'],
                    'unique_visitors': stat['unique_visitors']
                }
            )
        
        logger.info(f"Aggregated analytics for {len(daily_stats)} URLs")
        return len(daily_stats)
        
    except Exception as exc:
        logger.error(f"Error aggregating analytics: {exc}")
        raise


@shared_task
def cleanup_old_analytics():
    """Clean up old analytics data"""
    try:
        from django.conf import settings
        from shortener.models import Click
        
        retention_days = settings.ANALYTICS_RETENTION_DAYS
        cutoff_date = timezone.now() - timedelta(days=retention_days)
        
        deleted_count = Click.objects.filter(
            clicked_at__lt=cutoff_date
        ).delete()[0]
        
        logger.info(f"Deleted {deleted_count} old click records")
        return deleted_count
        
    except Exception as exc:
        logger.error(f"Error cleaning up analytics: {exc}")
        raise


@shared_task
def update_url_rankings():
    """Update URL rankings based on recent activity"""
    try:
        from shortener.models import URL
        from django.core.cache import cache
        
        # Get top URLs by clicks in last 7 days
        week_ago = timezone.now() - timedelta(days=7)
        
        top_urls = URL.objects.filter(
            is_active=True,
            click_records__clicked_at__gte=week_ago
        ).annotate(
            recent_clicks=Count('click_records')
        ).order_by('-recent_clicks')[:100]
        
        # Cache the rankings
        rankings = [
            {
                'short_code': url.short_code,
                'clicks': url.recent_clicks,
                'title': url.title
            }
            for url in top_urls
        ]
        
        cache.set('top_urls_weekly', rankings, 1800)  # Cache for 30 minutes
        
        logger.info(f"Updated rankings for {len(rankings)} URLs")
        return len(rankings)
        
    except Exception as exc:
        logger.error(f"Error updating rankings: {exc}")
        raise
