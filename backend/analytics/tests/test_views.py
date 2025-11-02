"""
Tests for analytics views
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestDashboardStatsView:
    """Tests for Dashboard Stats View"""
    
    def test_get_dashboard_stats(self, api_client, sample_url, sample_click):
        """Test getting dashboard statistics"""
        url = reverse('dashboard-stats')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'total_urls' in response.data
        assert 'total_clicks' in response.data
        assert 'total_unique_visitors' in response.data
        assert 'clicks_today' in response.data
        assert 'clicks_this_week' in response.data
        assert 'top_urls' in response.data
    
    def test_dashboard_stats_counts(self, api_client, sample_url):
        """Test dashboard stats has correct counts"""
        url = reverse('dashboard-stats')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_urls'] >= 1


@pytest.mark.django_db
class TestTrendsView:
    """Tests for Trends View"""
    
    def test_get_trends_default(self, api_client, sample_click):
        """Test getting trends with default period"""
        url = reverse('trends')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'period_days' in response.data
        assert 'trends' in response.data
        assert response.data['period_days'] == 30  # Default is 30
    
    def test_get_trends_custom_period(self, api_client):
        """Test getting trends with custom period"""
        url = reverse('trends')
        
        response = api_client.get(url, {'days': 7})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['period_days'] == 7
    
    def test_get_trends_large_period(self, api_client):
        """Test getting trends with large period (currently no validation)"""
        url = reverse('trends')
        
        response = api_client.get(url, {'days': 365})
        
        # Currently no validation, so it should succeed
        assert response.status_code == status.HTTP_200_OK
        assert response.data['period_days'] == 365
