"""
Tests for shortener views
"""
import pytest
from django.urls import reverse
from rest_framework import status
from shortener.models import URL


@pytest.mark.django_db
class TestURLViewSet:
    """Tests for URL ViewSet"""
    
    def test_create_url(self, api_client):
        """Test creating a new URL"""
        url = reverse('url-list')
        data = {
            'original_url': 'https://www.example.com/very/long/url',
            'title': 'Example Site'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'short_code' in response.data
        assert response.data['original_url'] == data['original_url']
        assert len(response.data['short_code']) == 8  # SHORT_CODE_LENGTH=8
    
    def test_create_url_with_custom_code(self, api_client):
        """Test creating URL with custom short code"""
        url = reverse('url-list')
        data = {
            'original_url': 'https://www.example.com',
            'custom_code': 'mycustom'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['short_code'] == 'mycustom'
    
    def test_create_url_invalid_url(self, api_client):
        """Test creating URL with invalid URL"""
        url = reverse('url-list')
        data = {
            'original_url': 'not-a-valid-url'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_url_duplicate_custom_code(self, api_client, sample_url):
        """Test creating URL with duplicate custom code"""
        url = reverse('url-list')
        data = {
            'original_url': 'https://www.new.com',
            'custom_code': sample_url.short_code  # Existing code
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_list_urls(self, api_client, sample_url):
        """Test listing URLs"""
        url = reverse('url-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
    
    def test_retrieve_url(self, api_client, sample_url):
        """Test retrieving a specific URL"""
        url = reverse('url-detail', kwargs={'pk': sample_url.pk})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['short_code'] == sample_url.short_code
    
    def test_update_url(self, api_client, sample_url):
        """Test updating a URL"""
        url = reverse('url-detail', kwargs={'pk': sample_url.pk})
        data = {
            'title': 'Updated Title'
        }
        
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
    
    def test_delete_url(self, api_client, sample_url):
        """Test soft deleting a URL (sets is_active=False)"""
        url = reverse('url-detail', kwargs={'pk': sample_url.pk})
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Soft delete - URL still exists but is_active=False
        sample_url.refresh_from_db()
        assert URL.objects.filter(pk=sample_url.pk).exists()
        assert sample_url.is_active is False
    
    def test_get_url_stats(self, api_client, sample_url, sample_click):
        """Test getting URL statistics"""
        url = reverse('url-stats', kwargs={'pk': sample_url.pk})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'total_clicks' in response.data
        assert 'unique_clicks' in response.data


@pytest.mark.django_db
class TestRedirectView:
    """Tests for redirect view"""
    
    def test_redirect_to_original_url(self, api_client, sample_url):
        """Test redirecting to original URL"""
        url = f'/{sample_url.short_code}/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == sample_url.original_url
    
    def test_redirect_expired_url(self, api_client, expired_url):
        """Test redirecting to expired URL returns 410"""
        url = f'/{expired_url.short_code}/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_410_GONE
    
    def test_redirect_nonexistent_code(self, api_client):
        """Test redirecting with nonexistent code returns 404"""
        url = '/nonexistent/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_redirect_inactive_url(self, api_client, sample_url):
        """Test redirecting to inactive URL returns 404"""
        from django.core.cache import cache
        
        # Clear cache to ensure is_active check works
        cache_key = f'url_{sample_url.short_code}'
        cache.delete(cache_key)
        
        sample_url.is_active = False
        sample_url.save()
        
        url = f'/{sample_url.short_code}/'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestHealthCheckView:
    """Tests for health check view"""
    
    def test_health_check(self, api_client):
        """Test health check endpoint"""
        url = reverse('health-check')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'healthy'
        assert 'timestamp' in response.data
