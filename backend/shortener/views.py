from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Q
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import qrcode
from io import BytesIO
import hashlib

from .models import URL, Click
from .serializers import (
    URLCreateSerializer,
    URLSerializer,
    URLListSerializer,
    URLStatsSerializer,
    ClickSerializer
)
from .tasks import track_click_async, generate_qr_code_async


class URLViewSet(viewsets.ModelViewSet):
    """
    ViewSet for URL shortening operations
    """
    queryset = URL.objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return URLCreateSerializer
        elif self.action == 'list':
            return URLListSerializer
        return URLSerializer
    
    @method_decorator(ratelimit(
        key='ip',
        rate=f'{settings.RATE_LIMIT_PER_MINUTE}/m',
        method='POST'
    ))
    def create(self, request, *args, **kwargs):
        """Create a new short URL"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.save()
        
        # Generate QR code asynchronously
        if url.id:
            generate_qr_code_async.delay(url.id)
        
        # Return the created URL
        return_serializer = URLSerializer(url, context={'request': request})
        return Response(
            return_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
        """List all short URLs with pagination"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Apply filters
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(original_url__icontains=search) |
                Q(short_code__icontains=search) |
                Q(title__icontains=search)
            )
        
        # Order by
        order_by = request.query_params.get('order_by', '-created_at')
        allowed_orders = ['created_at', '-created_at', 'clicks', '-clicks']
        if order_by in allowed_orders:
            queryset = queryset.order_by(order_by)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Get details of a specific short URL"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update a short URL"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete a short URL"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get detailed statistics for a URL"""
        url = self.get_object()
        
        # Get click data for last 30 days
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        clicks = Click.objects.filter(
            url=url,
            clicked_at__gte=thirty_days_ago
        )
        
        # Clicks by date
        clicks_by_date = clicks.values('clicked_at__date').annotate(
            count=Count('id')
        ).order_by('clicked_at__date')
        
        # Clicks by country
        clicks_by_country = dict(
            clicks.exclude(country__isnull=True)
            .values('country')
            .annotate(count=Count('id'))
            .values_list('country', 'count')
        )
        
        # Clicks by device
        clicks_by_device = dict(
            clicks.exclude(device_type__isnull=True)
            .values('device_type')
            .annotate(count=Count('id'))
            .values_list('device_type', 'count')
        )
        
        # Clicks by browser
        clicks_by_browser = dict(
            clicks.exclude(browser__isnull=True)
            .values('browser')
            .annotate(count=Count('id'))
            .values_list('browser', 'count')
        )
        
        # Top referrers
        top_referrers = list(
            clicks.exclude(referer__isnull=True)
            .values('referer')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        
        stats_data = {
            'total_clicks': url.clicks,
            'unique_clicks': url.unique_clicks,
            'last_accessed': url.last_accessed,
            'clicks_by_date': list(clicks_by_date),
            'clicks_by_country': clicks_by_country,
            'clicks_by_device': clicks_by_device,
            'clicks_by_browser': clicks_by_browser,
            'top_referrers': top_referrers,
        }
        
        serializer = URLStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def qrcode(self, request, pk=None):
        """Generate and return QR code for the short URL"""
        url = self.get_object()
        
        # Check if QR code is cached
        cache_key = f'qrcode_{url.short_code}'
        qr_image = cache.get(cache_key)
        
        if not qr_image:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url.get_short_url())
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            qr_image = buffer.getvalue()
            
            # Cache for 1 hour
            cache.set(cache_key, qr_image, 3600)
        
        return HttpResponse(qr_image, content_type='image/png')
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular URLs"""
        limit = int(request.query_params.get('limit', 10))
        queryset = self.get_queryset().order_by('-clicks')[:limit]
        serializer = URLListSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get most recent URLs"""
        limit = int(request.query_params.get('limit', 10))
        queryset = self.get_queryset().order_by('-created_at')[:limit]
        serializer = URLListSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class RedirectView(View):
    """Handle URL redirects"""
    
    def get(self, request, short_code):
        """Redirect to original URL and track the click"""
        
        # Try to get from cache first
        cache_key = f'url_{short_code}'
        url = cache.get(cache_key)
        
        if not url:
            url = get_object_or_404(
                URL,
                short_code=short_code,
                is_active=True
            )
            # Cache for 1 hour
            cache.set(cache_key, url, 3600)
        
        # Check if expired
        if url.is_expired():
            return HttpResponse(
                'This short URL has expired',
                status=410
            )
        
        # Track click asynchronously
        click_data = self.extract_click_data(request, url)
        track_click_async.delay(url.id, click_data)
        
        # Redirect to original URL
        return redirect(url.original_url)
    
    @staticmethod
    def extract_click_data(request, url):
        """Extract click data from request"""
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        # Generate session ID for unique visitor tracking
        session_string = f"{ip_address}_{request.META.get('HTTP_USER_AGENT', '')}"
        session_id = hashlib.md5(session_string.encode()).hexdigest()
        
        return {
            'ip_address': ip_address,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referer': request.META.get('HTTP_REFERER', ''),
            'session_id': session_id,
        }


class HealthCheckView(generics.GenericAPIView):
    """Health check endpoint"""
    
    def get(self, request):
        """Return service health status"""
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now().isoformat()
        })
