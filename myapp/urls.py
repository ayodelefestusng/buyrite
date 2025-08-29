# myproject/myapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # path('', home, name='home'),
   path('', HomeView.as_view(), name='home'),
   path('car/', car_view, name='car'),
         path('post/', create_post, name='create_post'),


]
    