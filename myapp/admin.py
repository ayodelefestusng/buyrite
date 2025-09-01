from django.contrib import admin

# # Register your models here.

# # Register your models here.
# from django.contrib import admin
# from .models import User,Category,Carousel,Tag,Post,Article

# # Register your models here.
# admin.site.register(User)
# admin.site.register(Category)
# admin.site.register(Carousel)
# admin.site.register(Post)
# admin.site.register(Tag)
# admin.site.register(Article)
# # admin.site.register(CustomUserManager)



# from django.contrib import admin
# from .models import Categorys, Brand, VehicleModel, Trim, ManufactureYear, Vehicle

# @admin.register(Categorys)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)

# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ('name',)

# @admin.register(VehicleModel)
# class VehicleModelAdmin(admin.ModelAdmin):
#     list_display = ('name', 'brand')
#     list_filter = ('brand',)

# @admin.register(Trim)
# class TrimAdmin(admin.ModelAdmin):
#     list_display = ('name', 'vehicle_model')
#     list_filter = ('vehicle_model',)

# @admin.register(ManufactureYear)
# class ManufactureYearAdmin(admin.ModelAdmin):
#     list_display = ('year',)

# @admin.register(Vehicle)
# class VehicleAdmin(admin.ModelAdmin):
#     list_display = ('brand', 'vehicle_model', 'trim', 'manufacture_year', 'price', 'is_available')
#     list_filter = ('category', 'brand', 'manufacture_year', 'is_available')
#     search_fields = ('description',)



from .models import (
    User, Category, Carousel, Tag, Post, Article,
    Categorys, Brand, VehicleModel, Trim, ManufactureYear,
    Condition, FuelOption, Color, EngineType, DriveTerrain,
    Vas, State, Town,InnerColor
)

from .models import Vehicle

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Carousel)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Trim)



admin.site.register(Categorys)
admin.site.register(Brand)
admin.site.register(VehicleModel)
admin.site.register(ManufactureYear)

admin.site.register(Condition)
admin.site.register(FuelOption)
admin.site.register(Color)
admin.site.register(InnerColor)
admin.site.register(EngineType)
admin.site.register(DriveTerrain)
admin.site.register(Vas)
admin.site.register(State)
admin.site.register(Town)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
       "pk", 'seller', 'brand', 'vehicle_model', 'trim', 'manufacture_year',
        'condition', 'fuel_option', 'color', 'engine_type', 'drive_terrain',
        'state', 'town', 'price', 'is_available',"slug"
    )
    list_filter = (
        'category', 'brand', 'manufacture_year', 'condition', 'fuel_option',
        'color', 'engine_type', 'drive_terrain', 'state', 'town', 'is_available'
    )
    # search_fields = ('description', 'contact_phone', 'social_media')
    search_fields = ['index', 'brand__name', 'vehicle_model__name', ]
    filter_horizontal = ('vas',)