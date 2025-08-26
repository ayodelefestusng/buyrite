from django.contrib import admin

# Register your models here.

# Register your models here.
from django.contrib import admin
from .models import User,Category

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
# admin.site.register(CustomUserManager)
