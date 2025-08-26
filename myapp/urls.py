# myproject/myapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
        path('car/', car_view, name='car'),


]
    