from rest_framework import serializers
from .models import Property, PropertyImage, PropertyInquiry, Favorite

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_primary', 'caption', 'created_at']

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'property_type', 'transaction_type',
            'price', 'area', 'bedrooms', 'bathrooms', 'floor', 'year_built',
            'address', 'city', 'postal_code', 'latitude', 'longitude',
            'is_featured', 'is_available', 'views_count', 'created_at',
            'updated_at', 'images', 'primary_image'
        ]
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None

class PropertyListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'property_type', 'transaction_type', 'price',
            'area', 'bedrooms', 'bathrooms', 'address', 'city',
            'is_featured', 'primary_image', 'created_at'
        ]
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None

class PropertyInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyInquiry
        fields = ['id', 'property', 'name', 'email', 'phone', 'message', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'property', 'created_at']