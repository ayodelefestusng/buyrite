from django.contrib import admin

# Register your models here.

# Register your models here.
from django.contrib import admin
from .models import User,Category,Carousel,Tag,Post

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Carousel)
admin.site.register(Post)
admin.site.register(Tag)
# admin.site.register(CustomUserManager)



from django.contrib import admin
from .models import Categorys, Brand, VehicleModel, Trim, ManufactureYear, Vehicle

@admin.register(Categorys)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    list_filter = ('brand',)

@admin.register(Trim)
class TrimAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_model')
    list_filter = ('vehicle_model',)

@admin.register(ManufactureYear)
class ManufactureYearAdmin(admin.ModelAdmin):
    list_display = ('year',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'vehicle_model', 'trim', 'manufacture_year', 'price', 'is_available')
    list_filter = ('category', 'brand', 'manufacture_year', 'is_available')
    search_fields = ('description',)