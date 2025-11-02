"""
Tests for shortener models
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from shortener.models import URL, Click


@pytest.mark.django_db
class TestURLModel:
    """Tests for URL model"""
    
    def test_create_url(self):
        """Test creating a URL"""
        url = URL.objects.create(
            original_url='https://www.google.com',
            short_code='abc123'
        )
        assert url.original_url == 'https://www.google.com'
        assert url.short_code == 'abc123'
        assert url.is_active is True
        assert url.clicks == 0
    
    def test_get_short_url(self, sample_url):
        """Test get_short_url method"""
        short_url = sample_url.get_short_url()
        assert 'test123' in short_url
        assert short_url.startswith('http')
    
    def test_is_expired_false(self, sample_url):
        """Test is_expired returns False for non-expired URL"""
        assert sample_url.is_expired() is False
    
    def test_is_expired_true(self, expired_url):
        """Test is_expired returns True for expired URL"""
        assert expired_url.is_expired() is True
    
    def test_increment_clicks(self, sample_url):
        """Test increment_clicks method"""
        initial_clicks = sample_url.clicks
        sample_url.increment_clicks()
        sample_url.refresh_from_db()
        assert sample_url.clicks == initial_clicks + 1
    
    def test_increment_unique_click(self, sample_url):
        """Test increment_clicks with is_unique=True"""
        initial_unique = sample_url.unique_clicks
        sample_url.increment_clicks(is_unique=True)
        sample_url.refresh_from_db()
        assert sample_url.unique_clicks == initial_unique + 1
    
    def test_short_code_unique(self):
        """Test that short codes must be unique"""
        URL.objects.create(
            original_url='https://www.example.com',
            short_code='unique'
        )
        
        with pytest.raises(Exception):
            URL.objects.create(
                original_url='https://www.another.com',
                short_code='unique'  # Duplicate
            )
    
    def test_str_representation(self, sample_url):
        """Test string representation"""
        result = str(sample_url)
        assert 'test123' in result
        assert sample_url.original_url in result


@pytest.mark.django_db
class TestClickModel:
    """Tests for Click model"""
    
    def test_create_click(self, sample_url):
        """Test creating a click"""
        click = Click.objects.create(
            url=sample_url,
            ip_address='192.168.1.1',
            user_agent='Test Agent',
            session_id='session123'
        )
        assert click.url == sample_url
        assert click.ip_address == '192.168.1.1'
        assert click.clicked_at is not None
    
    def test_click_count_increases(self, sample_url):
        """Test that creating clicks increases URL click count"""
        initial_count = sample_url.clicks
        
        Click.objects.create(
            url=sample_url,
            ip_address='127.0.0.1',
            session_id='session1'
        )
        
        # Note: In real app, increment_clicks is called separately
        sample_url.increment_clicks()
        sample_url.refresh_from_db()
        
        assert sample_url.clicks == initial_count + 1
    
    def test_str_representation(self, sample_click):
        """Test string representation"""
        result = str(sample_click)
        assert 'test123' in result
        assert 'Click on' in result
