"""
Pytest configuration and fixtures for the entire test suite
"""
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from shortener.models import URL, Click


@pytest.fixture
def api_client():
    """Create an API client for testing"""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def sample_url(db):
    """Create a sample URL for testing"""
    return URL.objects.create(
        original_url='https://www.example.com',
        short_code='test123',
        title='Test URL',
        is_active=True
    )


@pytest.fixture
def expired_url(db):
    """Create an expired URL for testing"""
    from django.utils import timezone
    from datetime import timedelta
    
    return URL.objects.create(
        original_url='https://www.expired.com',
        short_code='expired',
        expires_at=timezone.now() - timedelta(days=1),
        is_active=True
    )


@pytest.fixture
def sample_click(db, sample_url):
    """Create a sample click for testing"""
    return Click.objects.create(
        url=sample_url,
        ip_address='127.0.0.1',
        user_agent='Mozilla/5.0',
        session_id='test_session',
        country='US',
        city='New York'
    )
