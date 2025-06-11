from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
        ('office', 'Office'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
    ]
    
    TRANSACTION_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    
    # Price and Area
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.DecimalField(max_digits=8, decimal_places=2, help_text="Area in square meters")
    
    # Property Details
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=1)
    floor = models.IntegerField(null=True, blank=True)
    year_built = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1800), MaxValueValidator(2030)]
    )
    
    # Location
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Status and Features
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Properties"
    
    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'created_at']
    
    def __str__(self):
        return f"Image for {self.property.title}"
    
    def save(self, *args, **kwargs):
        # Ensure only one primary image per property
        if self.is_primary:
            PropertyImage.objects.filter(
                property=self.property, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)

class PropertyInquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Property Inquiries"
    
    def __str__(self):
        return f"Inquiry for {self.property.title} by {self.name}"

class Favorite(models.Model):
    user_session = models.CharField(max_length=100)  # For anonymous users
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user_session', 'property']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Favorite: {self.property.title}"