from django.urls import path
from . import views

urlpatterns = [
    path('properties/featured/', views.featured_properties, name='featured_properties'),
    path('properties/sale/', views.sale_properties, name='sale_properties'),
    path('properties/rent/', views.rent_properties, name='rent_properties'),
    path('properties/all/', views.all_properties, name='all_properties'),
]