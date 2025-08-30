import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


# Create your models here.
from django.db import models

# Create your models here.
# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings # Still needed if CustomUser remains primary for other features
from django.core.validators import MaxValueValidator
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
from django.core.exceptions import ValidationError
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db import models

# models.py
from django.db import models


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)  # ← Add this if missing
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # Role flags
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)


    # mfa_secret = models.CharField(max_length=16, blank=True, null=True)
    # mfa_enabled = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users_users',  # <-- Add this line
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users_user_permissions',  # <-- Add this line
        blank=True,
        help_text='Specific permissions for this user.'
    )


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.emai
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(('full name'), max_length=255)
    phone = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')

class Carousel(models.Model):
    name = models.CharField(unique=True,max_length=100)
    image = models.ImageField(upload_to='carosel_images/')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Orders categories alphabetically by name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)




# class Customer(AbstractUser):
#     is_seller = models.BooleanField(default=False)
#     is_buyer = models.BooleanField(default=True)
#     phone_number = models.CharField(max_length=20, blank=True)

# class VehicleCategory(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


# class Vehicle(models.Model):
#     seller = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True)
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     brand = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#     year = models.PositiveIntegerField()
#     mileage = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=12, decimal_places=2)
#     image = models.ImageField(upload_to='vehicles/')
#     is_available = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.brand} {self.model} ({self.year})"
    


class Categorys(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(unique=True,max_length=100)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Orders categories alphabetically by name

# Represents the manufacturer (e.g., Toyota, BMW).
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='vehicles/logo')

    def __str__(self):
        return self.name
    


# Linked to a brand (e.g., Corolla under Toyota).
class VehicleModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('brand', 'name')

    def __str__(self):
        # return f"{self.brand.name} {self.name}"
        return f"{self.name}"
    

# Specific version of a model (e.g., Corolla LE, Corolla XSE)
class Trim(models.Model):
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default=None)

    class Meta:
        unique_together = ('vehicle_model', 'name')

    def __str__(self):
        return f"{self.vehicle_model} {self.name}"
    
class ManufactureYear(models.Model):
    year = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.year)

class Condition(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class FuelOption(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Color(models.Model):
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

class Vas(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.name}"
    
BOOLEAN_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
]
TRANSMISSION_CHOICES = [
    ('automatic', 'Automatic'),
    ('manual', 'Manual'),
]
class Vehicle1(models.Model):
    # ForeignKey fields
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.SET_NULL, null=True)
    trim = models.ForeignKey(Trim, on_delete=models.SET_NULL, null=True)
    manufacture_year = models.ForeignKey(ManufactureYear, on_delete=models.SET_NULL, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True)
    fuel_option = models.ForeignKey(FuelOption, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    engine_type = models.ForeignKey(EngineType, on_delete=models.SET_NULL, null=True)
    drive_terrain = models.ForeignKey(DriveTerrain, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    town = models.ForeignKey(Town, on_delete=models.SET_NULL, null=True)

    # Boolean and numeric fields
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

    # Text and contact
    contact_phone = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    social_media = models.URLField(blank=True, null=True)

    # Many-to-many
    vas = models.ManyToManyField(Vas)

    # Image fields
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

    # Availability and tracking
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_sold = models.DateTimeField(blank=True, null=True)
    number_of_view = models.PositiveIntegerField(default=0)

    # Metadata
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    vin = models.CharField( max_length=50, blank=True)
    index = models.CharField(max_length=130, blank=True, unique=True, db_index=True)
   

    # def clean(self):
    #     super().clean()
    #     image_fields = [
    #         self.image, self.image2, self.image3, self.image4, self.image5,
    #         self.image6, self.image7, self.image8, self.image9, self.image10
    #     ]
    #     for image in image_fields:
    #         if image:
    #             img = Image.open(image)
    #             width, _ = img.size
    #             if width < 200 or width > 1000:
    #                 raise ValidationError(
    #                     f"Image '{image.name}' must be between 600 and 800 pixels wide. Current width: {width}px."
    #                 )
    # def clean(self):
    #     super().clean()
    #     image_fields = [
    #         self.image, self.image2, self.image3, self.image4, self.image5,
    #         self.image6, self.image7, self.image8, self.image9, self.image10
    #     ]
    #     for image in image_fields:
    #         if image:
    #             img = Image.open(image)
    #             width, _ = img.size
    #             if width < 200 or width > 1000:
    #                 raise ValidationError(
    #                     f"Image '{image.name}' must be between 200 and 1000 pixels wide. Current width: {width}px."
    #                 )
                
    # def save(self, *args, **kwargs):
    #     if not self.contact_phone and hasattr(self.seller, 'profile') and self.seller.profile.phone_number:
    #         self.contact_phone = self.seller.profile.phone_number

    #     if not self.date_sold:
    #         self.date_sold = timezone.now()

    #     self.full_clean()

    #     if not self.slug:
    #         base_slug = slugify(str(self.brand))
    #         slug = base_slug
    #         counter = 1
    #         while Vehicle.objects.filter(slug=slug).exists():
    #             slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = slug

    #     if not self.index:
    #         base_index = slugify(f"{self.brand.name}-{self.trim.name}-{self.category.name}-"
    #                              f"{self.manufacture_year.year}-{self.vehicle_model.name}-"
    #                              f"{self.condition.name}-{self.fuel_option.name}-"
    #                              f"{self.engine_type.name}-{self.drive_terrain.name}-"
    #                              f"{self.state.name}-{self.town.name}")
    #         index = base_index
    #         counter = 1
    #         while Vehicle.objects.filter(index=index).exists():
    #             index = f"{base_index}-{counter}"
    #             counter += 1
    #         self.index = index
            
    #     super().save(*args, **kwargs) # <-- Move this line outside the `if` block.
    # # def save(self, *args, **kwargs):
    # #     if not self.contact_phone and hasattr(self.seller, 'profile') and self.seller.profile.phone_number:
    # #         self.contact_phone = self.seller.profile.phone_number

    # #     if not self.date_sold:
    # #         self.date_sold = timezone.now()

    # #     self.full_clean()

    # #     if not self.slug:
    # #         base_slug = slugify(str(self.brand))
    # #         slug = base_slug
    # #         counter = 1
    # #         while Vehicle.objects.filter(slug=slug).exists():
    # #             slug = f"{base_slug}-{counter}"
    # #             counter += 1
    # #         self.slug = slug

    # #     if not self.index:
    # #         base_index = slugify(f"{self.brand.name}-{self.trim.name}-{self.category.name}-"
    # #                      f"{self.manufacture_year.year}-{self.vehicle_model.name}-"
    # #                      f"{self.condition.name}-{self.fuel_option.name}-"
    # #                      f"{self.engine_type.name}-{self.drive_terrain.name}-"
    # #                      f"{self.state.name}-{self.town.name}")
    # #         index = base_index
    # #         counter = 1
    # #         while Vehicle.objects.filter(index=index).exists():
    # #             index = f"{base_index}-{counter}"
    # #             counter += 1
    # #         self.index = index
    # #     super().save(*args, **kwargs)
    # class Vehicle(models.Model):
    # ... (all your existing fields are unchanged) ...

    def clean(self):
        super().clean()
        image_fields = [
            self.image, self.image2, self.image3, self.image4, self.image5,
            self.image6, self.image7, self.image8, self.image9, self.image10
        ]
        for image in image_fields:
            if image:
                # Add a check to ensure the file exists before opening
                if os.path.exists(image.path):
                    img = Image.open(image)
                    width, _ = img.size
                    if width < 200 or width > 1000:
                        raise ValidationError(
                            f"Image '{image.name}' must be between 200 and 1000 pixels wide. Current width: {width}px."
                        )
                # You might also want to handle cases where the file doesn't exist
                # which could happen with the temporary ContentFile objects.
                # The primary issue is the timing of when you call `full_clean`.

    def save(self, *args, **kwargs):
        if not self.contact_phone and hasattr(self.seller, 'profile') and self.seller.profile.phone_number:
            self.contact_phone = self.seller.profile.phone_number

        if not self.date_sold:
            self.date_sold = timezone.now()

        # Remove this line to prevent the circular dependency
        # self.full_clean()

        # if not self.slug:
        #     base_slug = slugify(str(self.brand))
        #     slug = base_slug
        #     counter = 1
        #     while Vehicle.objects.filter(slug=slug).exists():
        #         slug = f"{base_slug}-{counter}"
        #         counter += 1
        #     self.slug = slug
        if not self.slug:
        # Create a base slug from the brand and model names
            base_slug = slugify(f"{self.brand.name}-{self.vehicle_model.name}")
            slug = base_slug
            counter = 1
            # Loop to ensure the slug is unique
            while Vehicle.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if not self.index:
            base_index = slugify(f"{self.brand.name}-{self.trim.name}-{self.category.name}-"
                                f"{self.manufacture_year.year}-{self.vehicle_model.name}-"
                                f"{self.condition.name}-{self.fuel_option.name}-"
                                f"{self.engine_type.name}-{self.drive_terrain.name}-"
                                f"{self.state.name}-{self.town.name}")
            index = base_index
            counter = 1
            while Vehicle.objects.filter(index=index).exists():
                index = f"{base_index}-{counter}"
                counter += 1
            self.index = index
        
        super().save(*args, **kwargs)

    # ... (the rest of your methods are unchanged) ...
    def __str__(self):
        # return f"{self.brand.name} {self.vehicle_model.name} {self.trim.name} ({self.manufacture_year.year})"

        return self.slug


class Vehicle2(models.Model):
    # ForeignKey fields
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.SET_NULL, null=True)
    trim = models.ForeignKey(Trim, on_delete=models.SET_NULL, null=True)
    manufacture_year = models.ForeignKey(ManufactureYear, on_delete=models.SET_NULL, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True)
    fuel_option = models.ForeignKey(FuelOption, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    engine_type = models.ForeignKey(EngineType, on_delete=models.SET_NULL, null=True)
    drive_terrain = models.ForeignKey(DriveTerrain, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    town = models.ForeignKey(Town, on_delete=models.SET_NULL, null=True)

    # Boolean and numeric fields
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

    # Text and contact
    contact_phone = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    social_media = models.URLField(blank=True, null=True)

    # Many-to-many
    vas = models.ManyToManyField(Vas)

    # Image fields
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

    # Availability and tracking
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_sold = models.DateTimeField(blank=True, null=True)
    number_of_view = models.PositiveIntegerField(default=0)

    # Metadata
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    vin = models.CharField( max_length=50, blank=True)
    index = models.CharField(max_length=130, blank=True, unique=True, db_index=True)
   


    def clean(self):
        super().clean()
        image_fields = [
            self.image, self.image2, self.image3, self.image4, self.image5,
            self.image6, self.image7, self.image8, self.image9, self.image10
        ]
        
        for image in image_fields:
            if image:
                try:
                    img = Image.open(image.file)
                    width, _ = img.size
                    if not (200 <= width <= 1000):
                        raise ValidationError(
                            f"Image '{image.name}' must be between 200 and 1000 pixels wide. Current width: {width}px."
                        )
                except FileNotFoundError:
                    pass
                except Exception as e:
                    raise ValidationError(f"Could not validate image '{image.name}': {e}")
    
    def save(self, *args, **kwargs):
        is_new_instance = self._state.adding

        # Handle other fields first
        if not self.contact_phone and hasattr(self.seller, 'profile') and self.seller.profile.phone_number:
            self.contact_phone = self.seller.profile.phone_number

        if not self.date_sold and self.is_available:
            self.date_sold = timezone.now()
        elif not self.is_available:
            self.date_sold = None

        # Check if we need to generate slug and index on creation
        if is_new_instance:
            # Generate the slug
            base_slug = slugify(f"{self.brand.name}-{self.vehicle_model.name}")
            self.slug = base_slug
            counter = 1
            while Vehicle.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

            # Generate the index
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
        
        # Finally, save the object (only once!)
        super().save(*args, **kwargs)

    # def __str__(self):
        # return self.slug
    # ... (the rest of your methods are unchanged) ...
    def __str__(self):
        return f"{self.brand.name} {self.vehicle_model.name} {self.trim.name} ({self.manufacture_year.year})"

    #     return self.slug


from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from PIL import Image
import os

# Assuming these are defined elsewhere
# BOOLEAN_CHOICES = [('yes', 'Yes'), ('no', 'No')]
# TRANSMISSION_CHOICES = [('automatic', 'Automatic'), ('manual', 'Manual')]
# Assuming you have imported your other models (Category, Brand, etc.)


from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from PIL import Image
import os

# Assuming other models (Category, Brand, etc.) are defined above this class
# and BOOLEAN_CHOICES, TRANSMISSION_CHOICES, and related imports are correct.

class Vehicle(models.Model):
    # ForeignKey fields
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    vehicle_model = models.ForeignKey('VehicleModel', on_delete=models.SET_NULL, null=True)
    trim = models.ForeignKey('Trim', on_delete=models.SET_NULL, null=True)
    manufacture_year = models.ForeignKey('ManufactureYear', on_delete=models.SET_NULL, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.SET_NULL, null=True)
    fuel_option = models.ForeignKey('FuelOption', on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True)
    engine_type = models.ForeignKey('EngineType', on_delete=models.SET_NULL, null=True)
    drive_terrain = models.ForeignKey('DriveTerrain', on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True)
    town = models.ForeignKey('Town', on_delete=models.SET_NULL, null=True)

    # Boolean and numeric fields
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

    # Text and contact
    contact_phone = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    social_media = models.URLField(blank=True, null=True)

    # Many-to-many
    vas = models.ManyToManyField('Vas')

    # Image fields
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

    # Availability and tracking
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_sold = models.DateTimeField(blank=True, null=True)
    number_of_view = models.PositiveIntegerField(default=0)

    # Metadata
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    vin = models.CharField(max_length=50, blank=True)
    index = models.CharField(max_length=130, blank=True, unique=True, db_index=True)

    def clean(self):
        super().clean()
        image_fields = [
            self.image, self.image2, self.image3, self.image4, self.image5,
            self.image6, self.image7, self.image8, self.image9, self.image10
        ]
        
        for image in image_fields:
            if image:
                try:
                    img = Image.open(image.file)
                    width, _ = img.size
                    if not (200 <= width <= 1000):
                        raise ValidationError(
                            f"Image '{image.name}' must be between 200 and 1000 pixels wide. Current width: {width}px."
                        )
                except FileNotFoundError:
                    # This happens when a file is not yet saved to disk (e.g., during tests)
                    pass
                except Exception as e:
                    raise ValidationError(f"Could not validate image '{image.name}': {e}")
    
    def save(self, *args, **kwargs):
        # Determine if this is a new instance
        is_new_instance = self._state.adding

        # Set contact_phone if it's not provided
        if not self.contact_phone and hasattr(self.seller, 'phone'):
            self.contact_phone = self.seller.phone

        # Handle the date_sold logic
        if self.is_available and not self.date_sold:
            self.date_sold = timezone.now()
        elif not self.is_available:
            self.date_sold = None
        
        # Generate slug and index only when the instance is new
        if is_new_instance:
            # Generate the slug
            base_slug = slugify(f"{self.brand.name}-{self.vehicle_model.name}")
            self.slug = base_slug
            counter = 1
            while Vehicle.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

            # Generate the index
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
        
        # Finally, save the object to the database (only once!)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} {self.vehicle_model.name} {self.trim.name} ({self.manufacture_year.year})"




# class Vehicle(models.Model):
#     seller = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
#     vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.SET_NULL, null=True)
#     trim = models.ForeignKey(Trim, on_delete=models.SET_NULL, null=True)
#     manufacture_year = models.ForeignKey(ManufactureYear, on_delete=models.SET_NULL, null=True)
#     mileage = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=12, decimal_places=2)
#     description = models.TextField()
#     image = models.ImageField(upload_to='vehicles/')
#     is_available = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.brand.name} {self.vehicle_model.name} {self.trim.name} ({self.manufacture_year.year})"
    



from django.db import models
from django.utils.text import slugify

from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.TextField(blank=True, editable=False)  # Auto-generated summary
    slug = models.SlugField(unique=True, max_length=255,blank=True)
    author = models.CharField(max_length=100, default='Anonymous')  # Optional: Add author field
    published_date = models.DateTimeField(default=timezone.now)     # Optional: Add timestamp
    tags = models.ManyToManyField('Tag', blank=True)                # Optional: Add tagging

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

                # Auto-generate excerpt if not set
        if not self.excerpt:
            plain_text = self.content.strip().replace('\n', ' ')
            self.excerpt = plain_text[:250] + '...' if len(plain_text) > 250 else plain_text
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title