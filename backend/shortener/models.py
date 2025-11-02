from django.db import models
from django.core.validators import URLValidator
from django.utils import timezone
from hashids import Hashids
import random
import string


class URL(models.Model):
    """Model to store URL mappings with analytics"""
    
    original_url = models.URLField(
        max_length=2048,
        validators=[URLValidator()],
        db_index=True,
        help_text="The original long URL"
    )
    short_code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="The unique short code for the URL"
    )
    custom_code = models.BooleanField(
        default=False,
        help_text="Whether this is a custom short code"
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional title for the URL"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description"
    )
    
    # Analytics fields
    clicks = models.BigIntegerField(
        default=0,
        help_text="Total number of clicks"
    )
    unique_clicks = models.BigIntegerField(
        default=0,
        help_text="Number of unique visitors"
    )
    last_accessed = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last time the URL was accessed"
    )
    
    # Status fields
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the short URL is active"
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Optional expiration date"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the creator"
    )
    
    # QR Code
    qr_code = models.ImageField(
        upload_to='qr_codes/',
        null=True,
        blank=True,
        help_text="Generated QR code for the short URL"
    )
    
    class Meta:
        db_table = 'urls'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['short_code']),
            models.Index(fields=['created_at']),
            models.Index(fields=['-clicks']),
            models.Index(fields=['is_active', 'expires_at']),
        ]
    
    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"
    
    @staticmethod
    def generate_short_code(length=6):
        """Generate a random short code"""
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(characters, k=length))
            if not URL.objects.filter(short_code=code).exists():
                return code
    
    @staticmethod
    def generate_hashid_code(url_id):
        """Generate a short code using HashID"""
        hashids = Hashids(min_length=6, salt='url-shortener-salt')
        return hashids.encode(url_id)
    
    def is_expired(self):
        """Check if the URL has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def increment_clicks(self, is_unique=False):
        """Increment click count"""
        self.clicks = models.F('clicks') + 1
        if is_unique:
            self.unique_clicks = models.F('unique_clicks') + 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['clicks', 'unique_clicks', 'last_accessed'])
    
    def get_short_url(self):
        """Get the full short URL"""
        from django.conf import settings
        return f"{settings.BASE_URL}/{self.short_code}"


class Click(models.Model):
    """Model to track individual clicks for analytics"""
    
    url = models.ForeignKey(
        URL,
        on_delete=models.CASCADE,
        related_name='click_records',
        db_index=True
    )
    
    # Request information
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        blank=True,
        null=True
    )
    referer = models.URLField(
        max_length=2048,
        blank=True,
        null=True,
        help_text="HTTP referer"
    )
    
    # Geolocation (can be populated by background task)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    # Device information
    device_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="mobile, tablet, desktop, bot"
    )
    browser = models.CharField(max_length=100, blank=True, null=True)
    os = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamp
    clicked_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Session tracking
    session_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Used to identify unique visitors"
    )
    
    class Meta:
        db_table = 'clicks'
        ordering = ['-clicked_at']
        indexes = [
            models.Index(fields=['url', '-clicked_at']),
            models.Index(fields=['clicked_at']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        return f"Click on {self.url.short_code} at {self.clicked_at}"
