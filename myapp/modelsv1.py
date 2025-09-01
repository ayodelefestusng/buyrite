from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify
import hashlib

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VehicleModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

class Trim(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ManufactureYear(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)

class FuelOption(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name

class InnerColor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class EngineType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class DriveTerrain(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class VAS(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Value Added Service"
        verbose_name_plural = "Value Added Services"

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Town(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='towns')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class Vehicle(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    vehicle_model = models.ForeignKey('VehicleModel', on_delete=models.SET_NULL, null=True)
    trim = models.ForeignKey('Trim', on_delete=models.SET_NULL, null=True)
    manufacture_year = models.ForeignKey('ManufactureYear', on_delete=models.SET_NULL, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.SET_NULL, null=True)
    fuel_option = models.ForeignKey('FuelOption', on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True)
    inner_color = models.ForeignKey('InnerColor', on_delete=models.SET_NULL, null=True)
    engine_type = models.ForeignKey('EngineType', on_delete=models.SET_NULL, null=True)
    drive_terrain = models.ForeignKey('DriveTerrain', on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True)
    town = models.ForeignKey('Town', on_delete=models.SET_NULL, null=True)

    BOOLEAN_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    TRANSMISSION_CHOICES = [('automatic', 'Automatic'), ('manual', 'Manual')]
    exchange_option = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    registered = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    negotiable = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    no_of_tyres = models.PositiveIntegerField(default=4, validators=[MaxValueValidator(32)])
    seat = models.PositiveIntegerField(default=5, validators=[MaxValueValidator(80)])
    mileage = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, default='automatic')
    number_cylinder = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(20)])
    horsepower = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(200)])

    contact_phone = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    social_media = models.URLField(blank=True, null=True)

    vas = models.ManyToManyField('Vas')

    image = models.ImageField(upload_to='vehicles/')
    image2 = models.ImageField(upload_to='vehicles/')
    image3 = models.ImageField(upload_to='vehicles/')
    image4 = models.ImageField(upload_to='vehicles/')
    image5 = models.ImageField(upload_to='vehicles/')
    image6 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image7 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image8 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image9 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image10 = models.ImageField(upload_to='vehicles/', blank=True, null=True)

    # Hash fields for image uniqueness validation
    image_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image2_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image3_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image4_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image5_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image6_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image7_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image8_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image9_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image10_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_sold = models.DateTimeField(blank=True, null=True)
    number_of_view = models.PositiveIntegerField(default=0)

    slug = models.SlugField(unique=True, max_length=255, blank=True)
    vin = models.CharField(max_length=50, blank=True)
    index = models.CharField(max_length=130, blank=True, unique=True, db_index=True)

    def clean(self):
        super().clean()
        # This method can be used for other validation logic, but not for image uniqueness,
        # which is handled in the view.
        # ... (other clean logic from your provided model)

    def save(self, *args, **kwargs):
        is_new_instance = self._state.adding
        
        if not self.contact_phone and hasattr(self.seller, 'phone'):
            self.contact_phone = self.seller.phone

        if self.is_available and not self.date_sold:
            self.date_sold = timezone.now()
        elif not self.is_available:
            self.date_sold = None
        
        if is_new_instance:
            base_slug = slugify(f"{self.brand.name}-{self.vehicle_model.name}")
            self.slug = base_slug
            counter = 1
            while Vehicle.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

            base_index = slugify(f"{self.brand.name}-{self.trim.name}-{self.category.name}-"
                                 f"{self.manufacture_year.year}-{self.vehicle_model.name}-"
                                 f"{self.condition.name}-{self.fuel_option.name}-"
                                 f"{self.engine_type.name}-{self.drive_terrain.name}-"
                                 f"{self.state.name}-{self.town.name}")
            self.index = base_index
            counter = 1
            while Vehicle.objects.filter(index=self.index).exists():
                self.index = f"{base_index}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} {self.vehicle_model.name} {self.trim.name} ({self.manufacture_year.year})"
