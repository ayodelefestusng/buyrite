# myproject/myapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # path('', home, name='home'),
   path('', HomeView.as_view(), name='home'),
    path('vehicle_detail/<slug:slug>/', VehicleDetailView.as_view(), name='vehicle_detail'),

    # In myproject/urls.py or myapp/urls.py
# path('vehicle_detail/<int:pk>/', VehicleDetailView.as_view(), name='vehicle_detail'),
    #   path('details', MODEL_NAMEDetailView.as_view(), name='details'),
   path('car/', car_view, name='car'),
    path('post/', create_post, name='create_post'),




# path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='articles:detail'),
# path('articles/', ArticleListView.as_view(), name='articles:list'),


path('articles/', ArticleListView.as_view(), name='list'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='detail'),



    # operation
      path('upload/', upload_vehicle, name='upload_vehicle'),
    path('upload/success/', upload_vehicle_success, name='upload_vehicle_success'),
    # HTMX endpoints
    path('load_models/', load_models, name='load_models'),
    path('load_trims/', load_trims, name='load_trims'),
    path('load_towns/', load_towns, name='load_towns'),


]
    