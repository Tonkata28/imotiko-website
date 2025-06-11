from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    fields = ['image', 'alt_text', 'is_main']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'category', 'location', 'price', 'is_featured', 'created_at']
    list_filter = ['property_type', 'category', 'is_featured', 'created_at']
    list_editable = ['is_featured']
    search_fields = ['title', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'property_type', 'category')
        }),
        ('Location & Details', {
            'fields': ('location', 'bedrooms', 'bathrooms', 'area', 'price')
        }),
        ('Features', {
            'fields': ('is_featured',)
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [PropertyImageInline]

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'alt_text', 'is_main']
    list_filter = ['is_main']
    list_editable = ['is_main']