from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings # Still needed if CustomUser remains primary for other features
 
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



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)  # ← Add this if missing
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    # mfa_secret = models.CharField(max_length=16, blank=True, null=True)
    # mfa_enabled = models.BooleanField(default=False)


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

from django.db import models

class Category(models.Model):
    name = models.CharField(unique=True,max_length=100)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Orders categories alphabetically by name


class Carousel(models.Model):
    name = models.CharField(unique=True,max_length=100)
    image = models.ImageField(upload_to='carosel_images/')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Orders categories alphabetically by name




# models.py
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)





from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, blank=True)

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
    
# Represents the manufacturer (e.g., Toyota, BMW).
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

# Linked to a brand (e.g., Corolla under Toyota).
class VehicleModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('brand', 'name')

    def __str__(self):
        return f"{self.brand.name} {self.name}"
    

# Specific version of a model (e.g., Corolla LE, Corolla XSE)
class Trim(models.Model):
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('vehicle_model', 'name')

    def __str__(self):
        return f"{self.vehicle_model} {self.name}"
    
class ManufactureYear(models.Model):
    year = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.year)
    


class Vehicle(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.SET_NULL, null=True)
    trim = models.ForeignKey(Trim, on_delete=models.SET_NULL, null=True)
    manufacture_year = models.ForeignKey(ManufactureYear, on_delete=models.SET_NULL, null=True)
    mileage = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='vehicles/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand.name} {self.vehicle_model.name} {self.trim.name} ({self.manufacture_year.year})"