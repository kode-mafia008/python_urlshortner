"""
Tests for Celery tasks
"""
import pytest
from unittest.mock import Mock, patch
from shortener.tasks import track_click_async, generate_qr_code_async
from shortener.models import URL, Click


@pytest.mark.django_db
class TestTrackClickTask:
    """Tests for track_click_async task"""
    
    def test_track_click_creates_click(self, sample_url):
        """Test that track_click creates a Click object"""
        click_data = {
            'ip_address': '192.168.1.1',
            'user_agent': 'Test Agent',
            'session_id': 'test_session',
            'referer': 'https://google.com',
            'country': 'US',
            'city': 'New York'
        }
        
        initial_count = Click.objects.count()
        track_click_async(sample_url.id, click_data)
        
        assert Click.objects.count() == initial_count + 1
        click = Click.objects.latest('clicked_at')
        assert click.ip_address == '192.168.1.1'
        assert click.user_agent == 'Test Agent'
    
    def test_track_click_increments_url_clicks(self, sample_url):
        """Test that track_click increments URL clicks"""
        initial_clicks = sample_url.clicks
        
        click_data = {
            'ip_address': '192.168.1.1',
            'session_id': 'test_session'
        }
        
        track_click_async(sample_url.id, click_data)
        sample_url.refresh_from_db()
        
        assert sample_url.clicks == initial_clicks + 1
    
    def test_track_click_invalid_url(self):
        """Test track_click with invalid URL ID"""
        click_data = {'ip_address': '127.0.0.1'}
        
        with pytest.raises(Exception):
            track_click_async(99999, click_data)


@pytest.mark.django_db
class TestGenerateQRCodeTask:
    """Tests for generate_qr_code_async task"""
    
    @patch('shortener.tasks.qrcode.QRCode')
    def test_generate_qr_code(self, mock_qr, sample_url):
        """Test QR code generation"""
        mock_img = Mock()
        mock_qr.return_value.make_image.return_value = mock_img
        
        generate_qr_code_async(sample_url.id)
        
        assert mock_qr.called
        sample_url.refresh_from_db()
        # QR code should be set (mocked)
    
    def test_generate_qr_code_invalid_url(self):
        """Test QR code generation with invalid URL ID"""
        with pytest.raises(Exception):
            generate_qr_code_async(99999)
