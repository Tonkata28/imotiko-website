from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'properties', views.PropertyViewSet)

urlpatterns = [
    # Non-property related endpoints
    path('stats/', views.PropertyStatsView.as_view(), name='property-stats'),
    path('inquiries/', views.PropertyInquiryCreateView.as_view(), name='property-inquiries'),
    path('favorites/toggle/', views.FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite-list'),
    
    # Router includes all property endpoints
    path('', include(router.urls)),
]