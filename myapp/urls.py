# myproject/myapp/urls.py
from django.urls import path
from .views import *
# myapp/urls.py
from django.urls import path
from .views import DashboardView, mark_as_sold, edit_vehicle

urlpatterns = [
    # path('', home, name='home'),
   path('', HomeView.as_view(), name='home'),
     path('load-models/', load_models, name='load_models'),
    path('load-trims/', load_trims, name='load_trims'),
    path('load-years/', load_years, name='load_years'),

    

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
    # path('load_towns2/', load_towns2, name='load_towns2'),



  # Dashboard URL with an optional status parameter
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Endpoint to mark a vehicle as sold
    path('vehicle/<int:pk>/mark-as-sold/', mark_as_sold, name='mark_as_sold'),
    
    # Endpoint to edit a vehicle
    path('vehicle/<int:pk>/edit/', edit_vehicle, name='edit_vehicle'),


    # HTMX endpoints for dynamic filtering
    path('get-towns-by-state/<int:state_id>/', get_towns_by_state, name='get_towns_by_state'),
    path('get-models-by-brand/<int:brand_id>/', get_models_by_brand, name='get_models_by_brand'),


     # New Dealer Registration URLs
    path('dealer/register/', dealer_registration, name='dealer_registration'),


    
    # Operations Page and Admin Tools
    path('operations/', operations_view, name='operations'),
    path('operations/approve/<int:pk>/', approve_dealer, name='approve_dealer'),
    path('operations/reject/<int:pk>/', reject_dealer, name='reject_dealer'),
    path('operations/admin-tool/<str:model_name>/', handle_admin_tool_form, name='handle_admin_tool_form'),

#API
path("get-vehicle-image/", VehicleImageView.as_view(), name="get_vehicle_image"),
  path("api/vin-search/", VINImageSearchView.as_view(), name="vin_search")  ,
   path("api2/<str:vin>/", VINImageDrive, name="vin_drive")  
]



