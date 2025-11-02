from django.db import models


class DailyAnalytics(models.Model):
    """Aggregated daily analytics"""
    
    url = models.ForeignKey(
        'shortener.URL',
        on_delete=models.CASCADE,
        related_name='daily_analytics'
    )
    date = models.DateField(db_index=True)
    clicks = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'daily_analytics'
        unique_together = ['url', 'date']
        ordering = ['-date']
        indexes = [
            models.Index(fields=['url', '-date']),
        ]
    
    def __str__(self):
        return f"{self.url.short_code} - {self.date}: {self.clicks} clicks"
