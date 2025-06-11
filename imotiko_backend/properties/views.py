from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Property
import json

def property_to_dict(property_obj):
    """Convert Property object to dictionary for JSON response"""
    main_image = property_obj.images.filter(is_main=True).first()
    all_images = property_obj.images.all()
    
    return {
        'id': property_obj.id,
        'title': property_obj.title,
        'description': property_obj.description,
        'price': str(property_obj.price),
        'property_type': property_obj.property_type,
        'category': property_obj.category,
        'location': property_obj.location,
        'bedrooms': property_obj.bedrooms,
        'bathrooms': property_obj.bathrooms,
        'area': str(property_obj.area),
        'is_featured': property_obj.is_featured,
        'contact_phone': property_obj.contact_phone,
        'contact_email': property_obj.contact_email,
        'created_at': property_obj.created_at.isoformat(),
        'main_image': main_image.image.url if main_image else None,
        'images': [img.image.url for img in all_images],
    }

@csrf_exempt
@require_http_methods(["GET"])
def featured_properties(request):
    """API endpoint for featured properties (homepage top offers)"""
    properties = Property.objects.filter(is_featured=True).order_by('-created_at')
    data = [property_to_dict(prop) for prop in properties]
    
    return JsonResponse({
        'status': 'success',
        'count': len(data),
        'properties': data
    })

@csrf_exempt
@require_http_methods(["GET"])
def sale_properties(request):
    """API endpoint for properties for sale"""
    properties = Property.objects.filter(property_type='sale').order_by('-created_at')
    data = [property_to_dict(prop) for prop in properties]
    
    return JsonResponse({
        'status': 'success',
        'count': len(data),
        'properties': data
    })

@csrf_exempt
@require_http_methods(["GET"])
def rent_properties(request):
    """API endpoint for properties for rent"""
    properties = Property.objects.filter(property_type='rent').order_by('-created_at')
    data = [property_to_dict(prop) for prop in properties]
    
    return JsonResponse({
        'status': 'success',
        'count': len(data),
        'properties': data
    })

@csrf_exempt
@require_http_methods(["GET"])
def all_properties(request):
    """API endpoint for all properties"""
    properties = Property.objects.all().order_by('-created_at')
    data = [property_to_dict(prop) for prop in properties]
    
    return JsonResponse({
        'status': 'success',
        'count': len(data),
        'properties': data
    })