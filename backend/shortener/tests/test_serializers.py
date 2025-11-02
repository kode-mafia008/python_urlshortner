"""
Tests for shortener serializers
"""
import pytest
from shortener.serializers import (
    URLCreateSerializer,
    URLSerializer,
    URLListSerializer,
    ClickSerializer
)
from shortener.models import URL


@pytest.mark.django_db
class TestURLCreateSerializer:
    """Tests for URL Create Serializer"""
    
    def test_valid_url_creation(self):
        """Test creating a URL with valid data"""
        data = {
            'original_url': 'https://www.example.com'
        }
        serializer = URLCreateSerializer(data=data)
        
        assert serializer.is_valid()
        url = serializer.save()
        assert url.original_url == data['original_url']
        assert len(url.short_code) == 8
    
    def test_custom_code_validation(self):
        """Test custom code validation"""
        data = {
            'original_url': 'https://www.example.com',
            'custom_code': 'mycode'
        }
        serializer = URLCreateSerializer(data=data)
        
        assert serializer.is_valid()
        url = serializer.save()
        assert url.short_code == 'mycode'
    
    def test_invalid_url(self):
        """Test invalid URL"""
        data = {
            'original_url': 'not a url'
        }
        serializer = URLCreateSerializer(data=data)
        
        assert not serializer.is_valid()
        assert 'original_url' in serializer.errors
    
    def test_duplicate_custom_code(self, sample_url):
        """Test duplicate custom code"""
        data = {
            'original_url': 'https://www.example.com',
            'custom_code': sample_url.short_code
        }
        serializer = URLCreateSerializer(data=data)
        
        assert not serializer.is_valid()
        assert 'custom_code' in serializer.errors
    
    def test_custom_code_too_short(self):
        """Test custom code that's too short"""
        data = {
            'original_url': 'https://www.example.com',
            'custom_code': 'ab'  # Too short
        }
        serializer = URLCreateSerializer(data=data)
        
        assert not serializer.is_valid()
        assert 'custom_code' in serializer.errors
    
    def test_custom_code_invalid_characters(self):
        """Test custom code with invalid characters"""
        data = {
            'original_url': 'https://www.example.com',
            'custom_code': 'my-code!'  # Invalid characters
        }
        serializer = URLCreateSerializer(data=data)
        
        assert not serializer.is_valid()
        assert 'custom_code' in serializer.errors


@pytest.mark.django_db
class TestURLSerializer:
    """Tests for URL Serializer"""
    
    def test_serialize_url(self, sample_url):
        """Test serializing a URL"""
        from rest_framework.test import APIRequestFactory
        
        factory = APIRequestFactory()
        request = factory.get('/')
        
        serializer = URLSerializer(sample_url, context={'request': request})
        
        assert serializer.data['short_code'] == sample_url.short_code
        assert serializer.data['original_url'] == sample_url.original_url
        assert 'short_url' in serializer.data
        assert 'qr_code_url' in serializer.data
        assert 'is_expired' in serializer.data
    
    def test_short_url_field(self, sample_url):
        """Test short_url field generation"""
        from rest_framework.test import APIRequestFactory
        
        factory = APIRequestFactory()
        request = factory.get('/')
        
        serializer = URLSerializer(sample_url, context={'request': request})
        
        assert sample_url.short_code in serializer.data['short_url']


@pytest.mark.django_db
class TestURLListSerializer:
    """Tests for URL List Serializer"""
    
    def test_list_serializer_fields(self, sample_url):
        """Test list serializer has correct fields"""
        serializer = URLListSerializer(sample_url)
        
        assert 'id' in serializer.data
        assert 'short_code' in serializer.data
        assert 'original_url' in serializer.data
        assert 'title' in serializer.data
        assert 'clicks' in serializer.data
        assert 'created_at' in serializer.data


@pytest.mark.django_db
class TestClickSerializer:
    """Tests for Click Serializer"""
    
    def test_serialize_click(self, sample_click):
        """Test serializing a click"""
        serializer = ClickSerializer(sample_click)
        
        assert serializer.data['ip_address'] == sample_click.ip_address
        assert 'clicked_at' in serializer.data
        assert 'country' in serializer.data
        assert 'city' in serializer.data
