from celery import shared_task
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
import qrcode
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def track_click_async(self, url_id, click_data):
    """
    Track a click asynchronously
    """
    try:
        from .models import URL, Click
        from user_agents import parse
        
        url = URL.objects.get(id=url_id)
        
        # Parse user agent
        user_agent_string = click_data.get('user_agent', '')
        user_agent = parse(user_agent_string)
        
        # Determine device type
        device_type = 'desktop'
        if user_agent.is_mobile:
            device_type = 'mobile'
        elif user_agent.is_tablet:
            device_type = 'tablet'
        elif user_agent.is_bot:
            device_type = 'bot'
        
        # Check if this is a unique visitor
        session_id = click_data.get('session_id')
        is_unique = not Click.objects.filter(
            url=url,
            session_id=session_id
        ).exists()
        
        # Create click record
        with transaction.atomic():
            Click.objects.create(
                url=url,
                ip_address=click_data.get('ip_address'),
                user_agent=user_agent_string,
                referer=click_data.get('referer'),
                device_type=device_type,
                browser=user_agent.browser.family,
                os=user_agent.os.family,
                session_id=session_id,
            )
            
            # Update URL click count
            url.increment_clicks(is_unique=is_unique)
        
        logger.info(f"Click tracked for URL {url.short_code}")
        
    except Exception as exc:
        logger.error(f"Error tracking click: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def generate_qr_code_async(self, url_id):
    """
    Generate QR code for a URL asynchronously
    """
    try:
        from .models import URL
        
        url = URL.objects.get(id=url_id)
        
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
        buffer.seek(0)
        
        # Save QR code
        filename = f'{url.short_code}_qr.png'
        url.qr_code.save(filename, ContentFile(buffer.read()), save=True)
        
        logger.info(f"QR code generated for URL {url.short_code}")
        
    except Exception as exc:
        logger.error(f"Error generating QR code: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def cleanup_expired_urls():
    """
    Deactivate expired URLs
    """
    try:
        from .models import URL
        
        expired_count = URL.objects.filter(
            is_active=True,
            expires_at__lt=timezone.now()
        ).update(is_active=False)
        
        logger.info(f"Deactivated {expired_count} expired URLs")
        return expired_count
        
    except Exception as exc:
        logger.error(f"Error cleaning up expired URLs: {exc}")
        raise
