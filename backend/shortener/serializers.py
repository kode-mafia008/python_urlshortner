from rest_framework import serializers
from django.conf import settings
from .models import URL, Click
import validators


class URLCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating short URLs"""
    
    custom_code = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        help_text="Optional custom short code"
    )
    
    class Meta:
        model = URL
        fields = [
            'original_url',
            'custom_code',
            'title',
            'description',
            'expires_at'
        ]
    
    def validate_original_url(self, value):
        """Validate that the URL is properly formatted"""
        if not validators.url(value):
            raise serializers.ValidationError("Invalid URL format")
        return value
    
    def validate_custom_code(self, value):
        """Validate custom short code"""
        if value:
            if not settings.ENABLE_CUSTOM_CODES:
                raise serializers.ValidationError("Custom codes are not enabled")
            
            # Check if code is alphanumeric
            if not value.isalnum():
                raise serializers.ValidationError(
                    "Custom code must be alphanumeric"
                )
            
            # Check if code is available
            if URL.objects.filter(short_code=value).exists():
                raise serializers.ValidationError(
                    "This custom code is already taken"
                )
            
            # Check length
            if len(value) < 3 or len(value) > 20:
                raise serializers.ValidationError(
                    "Custom code must be between 3 and 20 characters"
                )
        
        return value
    
    def create(self, validated_data):
        """Create a new short URL"""
        custom_code = validated_data.pop('custom_code', None)
        
        # Generate or use custom short code
        if custom_code:
            validated_data['short_code'] = custom_code
            validated_data['custom_code'] = True
        else:
            validated_data['short_code'] = URL.generate_short_code(
                settings.SHORT_CODE_LENGTH
            )
            validated_data['custom_code'] = False
        
        # Get IP address from request context
        request = self.context.get('request')
        if request:
            validated_data['created_by_ip'] = self.get_client_ip(request)
        
        return super().create(validated_data)
    
    @staticmethod
    def get_client_ip(request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class URLSerializer(serializers.ModelSerializer):
    """Serializer for URL details"""
    
    short_url = serializers.SerializerMethodField()
    qr_code_url = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = URL
        fields = [
            'id',
            'original_url',
            'short_code',
            'short_url',
            'custom_code',
            'title',
            'description',
            'clicks',
            'unique_clicks',
            'last_accessed',
            'is_active',
            'expires_at',
            'is_expired',
            'created_at',
            'updated_at',
            'qr_code_url'
        ]
        read_only_fields = [
            'id',
            'short_code',
            'clicks',
            'unique_clicks',
            'last_accessed',
            'created_at',
            'updated_at'
        ]
    
    def get_short_url(self, obj):
        """Get the full short URL"""
        return obj.get_short_url()
    
    def get_qr_code_url(self, obj):
        """Get QR code URL if available"""
        if obj.qr_code:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
        return None
    
    def get_is_expired(self, obj):
        """Check if URL is expired"""
        return obj.is_expired()


class URLListSerializer(serializers.ModelSerializer):
    """Simplified serializer for URL list"""
    
    short_url = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = URL
        fields = [
            'id',
            'original_url',
            'short_code',
            'short_url',
            'title',
            'clicks',
            'is_active',
            'is_expired',
            'created_at'
        ]
    
    def get_short_url(self, obj):
        return obj.get_short_url()
    
    def get_is_expired(self, obj):
        return obj.is_expired()


class URLStatsSerializer(serializers.Serializer):
    """Serializer for URL statistics"""
    
    total_clicks = serializers.IntegerField()
    unique_clicks = serializers.IntegerField()
    last_accessed = serializers.DateTimeField()
    clicks_by_date = serializers.ListField()
    clicks_by_country = serializers.DictField()
    clicks_by_device = serializers.DictField()
    clicks_by_browser = serializers.DictField()
    top_referrers = serializers.ListField()


class ClickSerializer(serializers.ModelSerializer):
    """Serializer for click records"""
    
    class Meta:
        model = Click
        fields = [
            'id',
            'ip_address',
            'referer',
            'country',
            'city',
            'device_type',
            'browser',
            'os',
            'clicked_at'
        ]
        read_only_fields = fields
