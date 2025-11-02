from django.urls import path
from .views import DashboardStatsView, TrendsView

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('trends/', TrendsView.as_view(), name='trends'),
]
