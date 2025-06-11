from django.contrib import admin
from .models import Property, PropertyImage, PropertyInquiry, Favorite

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'is_primary', 'caption')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'property_type', 'transaction_type', 'price', 
        'city', 'is_featured', 'is_available', 'views_count', 'created_at'
    ]
    list_filter = [
        'property_type', 'transaction_type', 'city', 'is_featured', 
        'is_available', 'created_at'
    ]
    search_fields = ['title', 'address', 'city', 'description']
    list_editable = ['is_featured', 'is_available']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [PropertyImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'property_type', 'transaction_type')
        }),
        ('Price & Details', {
            'fields': ('price', 'area', 'bedrooms', 'bathrooms', 'floor', 'year_built')
        }),
        ('Location', {
            'fields': ('address', 'city', 'postal_code', 'latitude', 'longitude')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_available', 'views_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'is_primary', 'caption', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['property__title', 'caption']

@admin.register(PropertyInquiry)
class PropertyInquiryAdmin(admin.ModelAdmin):
    list_display = ['property', 'name', 'email', 'phone', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'property__title']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('property', 'message', 'is_read')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        })
    )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['property', 'user_session', 'created_at']
    list_filter = ['created_at']
    search_fields = ['property__title', 'user_session']
    readonly_fields = ['created_at']