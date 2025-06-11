from django.db import models
from PIL import Image
import os

class Property(models.Model):
    PROPERTY_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]
    
    PROPERTY_CATEGORIES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
        ('office', 'Office'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    category = models.CharField(max_length=20, choices=PROPERTY_CATEGORIES)
    location = models.CharField(max_length=200)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in square meters")
    
    # NEW: Featured field for homepage top offers
    is_featured = models.BooleanField(default=False, help_text="Show on homepage as top offer")
    
    # Contact information
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_property_type_display()}"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False, help_text="Main image for property")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if it's too large
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    def __str__(self):
        return f"Image for {self.property.title}"