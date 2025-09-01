from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect,
    HttpResponseServerError
)
from .models import *
from django.utils.timezone import now
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.apps import apps
from .models import (
    Vehicle, Category, State, Town, Brand, VehicleModel, Trim, DealerProfile, InnerColor,
    ManufactureYear, FuelOption, Color, EngineType, DriveTerrain, Vas
)
from django.contrib.auth import get_user_model
from .forms import VehicleForm, DealerRegistrationForm, AdminToolForm

# Create your views here.
# def home(request):
   
#    categories = Category.objects.all() 
#    carousels = Carousel.objects.all() 
#    context={"categories":categories,"carousels":carousels,}
#    return render(request,"home.html", context)

from django.views.generic import ListView,DetailView
from .models import Category, Carousel


from django.views.generic import ListView
from .models import Category, Carousel, Brand, VehicleModel, Trim, ManufactureYear, Vehicle
import hashlib
# class HomeView(ListView):
#     model = Category
#     template_name = 'home.html'
#     context_object_name = 'categories'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['carousels'] = Carousel.objects.all()
#         return context
    

def car_view(request):
    return render(request, 'car.html')


# views.py
from django.shortcuts import render, redirect
from .forms import PostForm

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your actual URL
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})



class MODEL_NAMEDetailView(DetailView):
    model = Category
    template_name = "details.html"
  
# In your app's views.py
from django.views.generic import DetailView
from .models import Article

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    slug_url_kwarg = 'slug' # Specify the URL keyword argument for the slug
 
    slug_field = 'slug' # Specify the model field to use for slug lookup
   




from django.views.generic import ListView
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10  # Optional: adds pagination
    ordering = ['-published_date']  # Newest first





# class HomeView(ListView):
#     model = Category
#     template_name = 'home.html'
#     context_object_name = 'categories'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Static content
#         context['carousels'] = Carousel.objects.all()
#         context['brands'] = Brand.objects.all()
#         context['models'] = VehicleModel.objects.all()
#         context['trims'] = Trim.objects.all()
#         context['years'] = ManufactureYear.objects.all()

#         context['posts'] = Post.objects.all()
#         context['alukuku'] = Vehicle.objects.all()

#         # Filtering logic
#         vehicles = Vehicle.objects.filter(is_available=True)

#         brand_id = self.request.GET.get('brand')
#         model_id = self.request.GET.get('model')
#         trim_id = self.request.GET.get('trim')
#         year_id = self.request.GET.get('year')

#         if brand_id:
#             vehicles = vehicles.filter(brand_id=brand_id)
#         if model_id:
#             vehicles = vehicles.filter(vehicle_model_id=model_id)
#         if trim_id:
#             vehicles = vehicles.filter(trim_id=trim_id)
#         if year_id:
#             vehicles = vehicles.filter(manufacture_year_id=year_id)

#         context['vehicles'] = vehicles
#         return context




from django.views.generic import ListView
from .models import Vehicle, Brand, Category, VehicleModel, Trim, ManufactureYear, Carousel, Post
from django.db.models import F

class HomeView1(ListView):
    model = Vehicle
    template_name = 'home.html'
    context_object_name = 'vehicles'
    paginate_by = 10  # Optional: Adds pagination for large lists

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_available=True).order_by('-created_at') # Add .order_by()
        brand_id = self.request.GET.get('brand')
        model_id = self.request.GET.get('model')
        trim_id = self.request.GET.get('trim')
        year_id = self.request.GET.get('year')
        
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if model_id:
            queryset = queryset.filter(vehicle_model_id=model_id)
        if trim_id:
            queryset = queryset.filter(trim_id=trim_id)
        if year_id:
            queryset = queryset.filter(manufacture_year_id=year_id)

        # Prefetch related objects to avoid N+1 query problem
        queryset = queryset.select_related('brand', 'vehicle_model', 'trim', 'manufacture_year', 'condition', 'fuel_option', 'color', 'engine_type', 'drive_terrain', 'state', 'town', 'category').prefetch_related('vas')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pass filter options for the search forms
        context['brands'] = Brand.objects.all()
        context['models'] = VehicleModel.objects.all()
        context['trims'] = Trim.objects.all()
        context['years'] = ManufactureYear.objects.all()
        context['categories'] = Category.objects.all()
        
        # Pass static content that's not related to the main vehicle list
        context['carousels'] = Carousel.objects.all()
        context['posts'] = Post.objects.all()
        
        return context

# myapp/views.py
from django.shortcuts import render
from django.views.generic import ListView
from myapp.models import (
    Vehicle, Brand, VehicleModel, Trim, ManufactureYear,
    Category, Carousel, Post
)
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string

# myapp/views.py
from django.shortcuts import render
from django.views.generic import ListView
from myapp.models import (
    Vehicle, Brand, VehicleModel, Trim, ManufactureYear,
    State, Town, Category, Carousel, Post
)
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string


class HomeViewV1(ListView):
    model = Vehicle
    template_name = 'myapp/home.html'
    context_object_name = 'vehicles'
    paginate_by = 10

    def get_queryset(self):
        # queryset = super().get_queryset().filter(is_available=True).order_by('-created_at')
        queryset = Vehicle.objects.filter(is_available=True).order_by('-created_at')

        
        # Get filter parameters from the request
        brand_id = self.request.GET.get('brand')
        model_id = self.request.GET.get('model')
        trim_id = self.request.GET.get('trim')
        state_id = self.request.GET.get('state')
        town_id = self.request.GET.get('town')
        category_id = self.request.GET.get('category')
        color = self.request.GET.get('color')
        inner_color = self.request.GET.get('inner_color')

        
        # New filters for price and year range
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        year_min = self.request.GET.get('year_min')
        year_max = self.request.GET.get('year_max')

       

        # Apply filters
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if model_id:
            queryset = queryset.filter(vehicle_model_id=model_id)
        if trim_id:
            queryset = queryset.filter(trim_id=trim_id)
        if state_id:
            queryset = queryset.filter(state_id=state_id)
        if town_id:
            queryset = queryset.filter(town_id=town_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if color:
            queryset = queryset.filter(color=color)
        if inner_color:
            queryset = queryset.filter(inner_color=inner_color)

 




        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        
        # Use Q objects for inclusive year range filter
        year_filter = Q()
        if year_min and year_max:
            year_filter = Q(manufacture_year__year__range=(year_min, year_max))
        elif year_min:
            year_filter = Q(manufacture_year__year__gte=year_min)
        elif year_max:
            year_filter = Q(manufacture_year__year__lte=year_max)

        queryset = queryset.filter(year_filter)

        # Prefetch related objects to avoid N+1 query problem
        queryset = queryset.select_related(
            'brand', 'vehicle_model', 'trim', 'manufacture_year', 'condition',
            'fuel_option', 'color', 'engine_type', 'drive_terrain',
            'state', 'town', 'category'
        ).prefetch_related('vas')
        
        return queryset

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.apps import apps
import hashlib
from .models import (
    Vehicle, Category, State, Town, Brand, VehicleModel, Trim, DealerProfile, InnerColor,
    ManufactureYear, FuelOption, Color, EngineType, DriveTerrain, Vas, Condition
)
from django.contrib.auth import get_user_model
from .forms import VehicleForm, DealerRegistrationForm, AdminToolForm

User = get_user_model()

class HomeView(ListView):
    model = Vehicle
    template_name = 'myapp/home.html'
    context_object_name = 'vehicles'
    
    def get_queryset(self):
        queryset = Vehicle.objects.filter(is_available=True).order_by('-created_at')
        
        category_id = self.request.GET.get('category')
        state_id = self.request.GET.get('state')
        town_id = self.request.GET.get('town')
        brand_id = self.request.GET.get('brand')
        model_id = self.request.GET.get('model')
        trim_id = self.request.GET.get('trim')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        color = self.request.GET.get('color')
        inner_color = self.request.GET.get('inner_color')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if state_id:
            queryset = queryset.filter(state_id=state_id)
        if town_id:
            queryset = queryset.filter(town_id=town_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if model_id:
            queryset = queryset.filter(vehicle_model_id=model_id)
        if trim_id:
            queryset = queryset.filter(trim_id=trim_id)
        if min_year:
            queryset = queryset.filter(manufacture_year__gte=min_year)
        if max_year:
            queryset = queryset.filter(manufacture_year__lte=max_year)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if color:
            queryset = queryset.filter(color=color)
        if inner_color:
            queryset = queryset.filter(inner_color=inner_color)
        
        return queryset.select_related('brand', 'vehicle_model', 'trim')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['states'] = State.objects.all()
        context['inner_colors'] = InnerColor.objects.all()
        context['colors'] = Vehicle.objects.values_list('color', flat=True).distinct()
        return context



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass filter options for the search forms
        context['brands'] = Brand.objects.all()
        context['states'] = State.objects.all()
        context['years'] = ManufactureYear.objects.all().order_by('-year')
        context['categories'] = Category.objects.all()

        # Pass static content that's not related to the main vehicle list
        context['carousels'] = Carousel.objects.all()
        # context['categories'] = Category.objects.all()
        context['posts'] = Post.objects.all()

        # Pre-select values for persistent filtering
        context['selected_brand'] = self.request.GET.get('brand')
        context['selected_model'] = self.request.GET.get('model')
        context['selected_trim'] = self.request.GET.get('trim')
        context['selected_state'] = self.request.GET.get('state')
        context['selected_town'] = self.request.GET.get('town')
        context['selected_category'] = self.request.GET.get('category')

        context['price_min'] = self.request.GET.get('price_min')
        context['price_max'] = self.request.GET.get('price_max')
        context['year_min'] = self.request.GET.get('year_min')
        context['year_max'] = self.request.GET.get('year_max')

        # Provide a queryset for the dynamic models/trims
        if context['selected_brand']:
            context['models'] = VehicleModel.objects.filter(brand_id=context['selected_brand'])
        else:
            context['models'] = VehicleModel.objects.none()

        if context['selected_model']:
            context['trims'] = Trim.objects.filter(vehicle_model_id=context['selected_model'])
        else:
            context['trims'] = Trim.objects.none()

        if context['selected_state']:
            context['towns'] = Town.objects.filter(state_id=context['selected_state'])
        else:
            context['towns'] = Town.objects.none()

        # Add 'created_ago' to each vehicle in the paginated list
        for vehicle in context['vehicles']:
            time_diff = now() - vehicle.created_at
            days = time_diff.days
            hours = time_diff.seconds // 3600

            if hours < 1:
                vehicle.created_ago = "Just now"
            elif days == 0:
                vehicle.created_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif days == 1:
                vehicle.created_ago = "1 day ago"
            else:
                vehicle.created_ago = f"{days} days ago"

        return context



def load_models(request):
    brand_id = request.GET.get('brand')
    models = VehicleModel.objects.filter(brand_id=brand_id).order_by('name')
    return render(request, 'myapp/partials/model_dropdown.html', {'models': models})

def load_trims(request):
    model_id = request.GET.get('model')
    trims = Trim.objects.filter(vehicle_model_id=model_id).order_by('name')
    return render(request, 'myapp/partials/trim_dropdown.html', {'trims': trims})
    
def load_towns(request):
    state_id = request.GET.get('state')
    towns = Town.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'myapp/partials/town_dropdown.html', {'towns': towns})

def load_models(request):
    brand_id = request.GET.get('brand')
    models = VehicleModel.objects.filter(brand_id=brand_id).order_by('name')
    return render(request, 'myapp/partials/model_dropdown.html', {'models': models})

def load_trims(request):
    model_id = request.GET.get('model')
    trims = Trim.objects.filter(vehicle_model_id=model_id).order_by('name')
    return render(request, 'myapp/partials/trim_dropdown.html', {'trims': trims})

def load_years(request):
    year_type = request.GET.get('type')
    years = ManufactureYear.objects.all().order_by('-year')
    return render(request, 'myapp/partials/year_dropdown.html', {'years': years, 'year_type': year_type})




from django.db.models import F

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle_detail.html'
    slug_url_kwarg = 'slug'
    # pk_url_kwarg = 'pk' 
    slug_field = 'slug'

    def get_object(self, queryset=None):
        # Use a database-level update for better performance and to prevent race conditions
        obj = super().get_object(queryset)
        # Vehicle.objects.filter(slug=self.kwargs.get('slug')).update(number_of_view=F('number_of_view') + 1)
        
        # Vehicle.objects.filter(pk=obj.pk).update(number_of_view=F('number_of_view') + 1)
        Vehicle.objects.filter(slug=obj.slug).update(number_of_view=F('number_of_view') + 1)


        # Now, retrieve the updated object to pass to the template
        return super().get_object(queryset)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.get_object()

        # Collect all non-empty image fields
        image_fields = [
            vehicle.image, vehicle.image2, vehicle.image3, vehicle.image4, vehicle.image5,
            vehicle.image6, vehicle.image7, vehicle.image8, vehicle.image9, vehicle.image10
        ]
        context['carousel'] = [img for img in image_fields if img]
        context['product_info'] = vehicle
        time_diff = now() - vehicle.created_at
        days = time_diff.days
        hours = time_diff.seconds // 3600

        # Format based on age
        if hours < 1.00001:
            created_ago = f"{hours} hour ago"
        elif days == 0:
            created_ago = f"{hours} hours ago"
        elif days == 1:
            created_ago = "1 day ago"
        else:
            created_ago = f"{days} days ago"


        context['created_ago'] = created_ago
        return context

#Gemini 
# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import VehicleForm
from .models import VehicleModel, Trim, Town, Vehicle, User
from django.template.loader import render_to_string
from django.contrib import messages

@login_required
def upload_vehicle11(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.seller = request.user # Automatically link the logged-in user
            
            # Auto-populate contact_phone if not provided and user has a phone number
            if not vehicle.contact_phone and hasattr(request.user, 'phone') and request.user.phone:
                vehicle.contact_phone = request.user.phone

            vehicle.save()
            form.save_m2m() # Save ManyToMany relationships after the main object is saved
            messages.success(request, 'Vehicle uploaded successfully!')
            return redirect('upload_vehicle_success') # Redirect to a success page or list
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VehicleForm()
        # Initial querysets for dynamic fields when form is first loaded (GET request)
        # These will be empty or set to defaults
        form.fields['vehicle_model'].queryset = VehicleModel.objects.none()
        form.fields['trim'].queryset = Trim.objects.none()
        form.fields['town'].queryset = Town.objects.none()

    return render(request, 'myapp/upload_vehicle.html', {'form': form})

# HTMX endpoints for dynamic dropdowns

def load_models(request):
    brand_id = request.GET.get('brand') # The name attribute of the select element
    models = VehicleModel.objects.filter(brand_id=brand_id).order_by('name')
    # Render partial HTML for vehicle_model select field
    html = render_to_string('myapp/partials/vehicle_model_options.html', {'models': models})
    # HTMX expects the entire updated element, not just options
    return HttpResponse(f'<div id="div_id_vehicle_model" class="mb-3">{html}</div>')

def load_trims(request):
    model_id = request.GET.get('vehicle_model') # The name attribute of the select element
    trims = Trim.objects.filter(vehicle_model_id=model_id).order_by('name')
    # Render partial HTML for trim select field
    html = render_to_string('myapp/partials/trim_options.html', {'trims': trims})
    return HttpResponse(f'<div id="div_id_trim" class="mb-3">{html}</div>')

def load_towns(request):
    state_id = request.GET.get('state') # The name attribute of the select element
    towns = Town.objects.filter(state_id=state_id).order_by('name')
    # Render partial HTML for town select field
    html = render_to_string('myapp/partials/town_options.html', {'towns': towns})
    return HttpResponse(f'<div id="div_id_town" class="mb-3">{html}</div>')


def load_towns2(request):
    """
    Returns a list of towns for the given state as an HTML snippet.
    """
    state_id = request.GET.get('state')
    towns = Town.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'home/town_options.html', {'towns': towns})


@login_required
def upload_vehicle_success(request):
    return render(request, 'myapp/upload_success.html')



# myapp/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

from .models import Vehicle
from .forms import VehicleForm1
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Vehicle, Category, State, Town, Brand, VehicleModel, Trim
from .forms import VehicleForm

@method_decorator(login_required, name='dispatch')
class DashboardView(ListView):
    model = Vehicle
    template_name = 'myapp/dashboard.html'
    context_object_name = 'vehicles'
    
    def get_queryset(self):
        status = self.request.GET.get('status', 'unsold')


        # Retrieve all filter parameters from the request
        status = self.request.GET.get('status', 'unsold')
        category_id = self.request.GET.get('category')
        state_id = self.request.GET.get('state')
        town_id = self.request.GET.get('town')
        brand_id = self.request.GET.get('brand')
        model_id = self.request.GET.get('model')
        trim_id = self.request.GET.get('trim')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        color = self.request.GET.get('color')
        inner_color = self.request.GET.get('inner_color')

        user = self.request.user
        
        # Superuser can see all vehicles; regular users only see their own
        if user.is_superuser:
            queryset = Vehicle.objects.all().order_by('-created_at')
        else:
            queryset = Vehicle.objects.filter(owner=user).order_by('-created_at')

        # Filter based on the selected status
        if status == 'sold':
            queryset = queryset.filter(is_available=False)
        elif status == 'unsold':
            queryset = queryset.filter(is_available=True)
        # If status is 'all', no additional filter is applied.


         # Apply other filters if present
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if state_id:
            queryset = queryset.filter(state_id=state_id)
        if town_id:
            queryset = queryset.filter(town_id=town_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if model_id:
            queryset = queryset.filter(vehicle_model_id=model_id)
        if trim_id:
            queryset = queryset.filter(trim_id=trim_id)
        if min_year:
            queryset = queryset.filter(manufacture_year__gte=min_year)
        if max_year:
            queryset = queryset.filter(manufacture_year__lte=max_year)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if color:
            queryset = queryset.filter(color=color)
        if inner_color:
            queryset = queryset.filter(inner_color=inner_color)
        
        
        
        return queryset.select_related('brand', 'vehicle_model', 'trim')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status', 'unsold')
        user = self.request.user

        # Get counts for the icon section
        if user.is_superuser:
            all_vehicles_count = Vehicle.objects.count()
            sold_count = Vehicle.objects.filter(is_available=False).count()
            unsold_count = Vehicle.objects.filter(is_available=True).count()
        else:
            all_vehicles_count = Vehicle.objects.filter(owner=user).count()
            sold_count = Vehicle.objects.filter(owner=user, is_available=False).count()
            unsold_count = Vehicle.objects.filter(owner=user, is_available=True).count()

        context['sold_count'] = sold_count
        context['unsold_count'] = unsold_count
        context['all_vehicles_count'] = all_vehicles_count
        context['current_status'] = status

        # Data for the filter form
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['states'] = State.objects.all()
        context['trims'] = Trim.objects.all()
        context['inner_colors'] = InnerColor.objects.all()
        context['colors'] = Vehicle.objects.values_list('color', flat=True).distinct()

    

         # Get selected values to pre-populate the filter form
        context['selected_state'] = self.request.GET.get('state')
        context['selected_brand'] = self.request.GET.get('brand')
        context['selected_category'] = self.request.GET.get('category')
        context['selected_trim'] = self.request.GET.get('trim')
        context['selected_min_year'] = self.request.GET.get('min_year')
        context['selected_max_year'] = self.request.GET.get('max_year')
        context['selected_min_price'] = self.request.GET.get('min_price')
        context['selected_max_price'] = self.request.GET.get('max_price')
        
        return context


@login_required
def mark_as_sold(request, pk):
    """Marks a vehicle as sold and returns the updated vehicle list."""
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicle, pk=pk)
        
        # Security check: Only allow the owner or a superuser to mark as sold
        if request.user == vehicle.seller or request.user.is_superuser:
            print ("Auo",pk)
            vehicle.is_available = False
            vehicle.save()
            return HttpResponse(status=200) # HTMX expects a success response
        
        return HttpResponse('Unauthorized', status=403)
    return HttpResponse('Invalid Request', status=400)


@login_required
def edit_vehicle(request, pk):
    """Handles vehicle editing via a form in a modal."""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    # Security check: Only allow the owner or a superuser to edit
    if request.user != vehicle.seller and not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=403)
        
    if request.method == 'POST':
        form = VehicleForm1(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            # On successful edit, return a new rendered vehicle card for HTMX swap
            return render(request, 'myapp/partials/_vehicle_card.html', {'vehicle': vehicle})
        else:
            # If form is invalid, return the form with errors for HTMX to re-render
            return render(request, 'myapp/partials/_edit_vehicle_modal.html', {'form': form, 'vehicle': vehicle})
    else:
        form = VehicleForm1(instance=vehicle)

    return render(request, 'myapp/partials/_edit_vehicle_modal.html', {'form': form, 'vehicle': vehicle})



@login_required
def upload_vehiclev1(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, "Vehicle uploaded successfully!")
            return redirect('dashboard')
    else:
        form = VehicleForm()
    
    context = {
        'form': form,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'states': State.objects.all(),
        'trims': Trim.objects.all(),
        'inner_colors': InnerColor.objects.all()
    }
    return render(request, 'myapp/upload_vehicle.html', context)

@login_required
def upload_vehicle(request):
    """
    Handles the vehicle upload form submission, including image duplicate checks.
    
    The view provides the necessary context for dynamic form fields, ensuring
    the HTMX functionality works correctly on both GET and invalid POST requests.
    """
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            # List of image fields to check
            image_fields = ['image', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9', 'image10']
            
            # Temporary set to hold hashes of newly uploaded images for intra-upload check
            uploaded_hashes = set()
            
            # Check for intra-upload duplicates and database duplicates
            for field_name in image_fields:
                uploaded_file = request.FILES.get(field_name)
                if uploaded_file:
                    hasher = hashlib.sha256()
                    for chunk in uploaded_file.chunks():
                        hasher.update(chunk)
                    image_hash = hasher.hexdigest()
                    
                    if image_hash in uploaded_hashes:
                        messages.error(request, "Please upload distinct images. A duplicate was found among the uploaded files.")
                        return redirect('dashboard')
                    
                    # Check database for existing hash in any image field
                    # The Q object is used to build a complex query across multiple fields
                    q_objects = Q()
                    for hash_field in [f'{f}_hash' for f in image_fields]:
                        q_objects |= Q(**{hash_field: image_hash})
                    
                    if Vehicle.objects.filter(q_objects).exists():
                        messages.error(request, "This photo already exists in the database.")
                        return redirect('dashboard')
                    
                    uploaded_hashes.add(image_hash)
            
            # Save the vehicle and its image hashes
            vehicle = form.save(commit=False)
            vehicle.seller = request.user
            
            # Manually set the image hash fields
            for field_name in image_fields:
                uploaded_file = request.FILES.get(field_name)
                if uploaded_file:
                    hasher = hashlib.sha256()
                    for chunk in uploaded_file.chunks():
                        hasher.update(chunk)
                    image_hash = hasher.hexdigest()
                    setattr(vehicle, f'{field_name}_hash', image_hash)
            
            vehicle.save()
            form.save_m2m()
            
            messages.success(request, "Vehicle uploaded successfully!")
            return redirect('dashboard')
        else:
            context = {
                'form': form,
                'brands': Brand.objects.all(),
                'categories': Category.objects.all(),
                'states': State.objects.all(),
                'trims': Trim.objects.all(),
                'inner_colors': InnerColor.objects.all()
            }
            messages.error(request, "There was an error in your submission. Please check the form and try again.")
            return render(request, 'myapp/upload_vehicle.html', context)
    else:
        form = VehicleForm()
    
    context = {
        'form': form,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'states': State.objects.all(),
        'trims': Trim.objects.all(),
        'inner_colors': InnerColor.objects.all()
    }
    return render(request, 'myapp/upload_vehicle.html', context)





def get_towns_by_state(request, state_id):
    """Returns a partial HTML for towns based on the selected state."""
    towns = Town.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'myapp/partials/_dynamic_towns.html', {'towns': towns})


def get_models_by_brand(request, brand_id):
    """Returns a partial HTML for models based on the selected brand."""
    models = VehicleModel.objects.filter(brand_id=brand_id).order_by('name')
    return render(request, 'myapp/partials/_dynamic_models.html', {'models': models})


@login_required
def dealer_registration(request):
    """
    Handles the dealer registration form submission.
    """
    # Check if the user is already a dealer
    if DealerProfile.objects.filter(user=request.user).exists():
        messages.info(request, "You are already registered as a dealer.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = DealerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            dealer_profile = form.save(commit=False)
            dealer_profile.user = request.user
            dealer_profile.save()
            
            messages.success(request, "You have successfully registered as a dealer! You can now list vehicles.")
            return redirect('dashboard')
    else:
        form = DealerRegistrationForm()

    context = {
        'form': form,
        'states': State.objects.all(),
    }
    return render(request, 'myapp/dealer_reg.html', context)


@login_required
@permission_required('auth.add_user', raise_exception=True)
def operations_view(request):
    """
    Displays the Operations dashboard for Managers and Superusers.
    
    This view lists dealers who are pending approval, rejected, and approved.
    It also provides access to admin tools based on user permissions.
    """
    unconfirmed_dealers = DealerProfile.objects.filter(is_confirmed=False)
    rejected_dealers = DealerProfile.objects.filter(is_confirmed=False, is_rejected=True)
    approved_dealers = DealerProfile.objects.filter(is_confirmed=True)

    models_to_manage = [
        ('Category', Category),
        ('Brand', Brand),
        ('VehicleModel', VehicleModel),
        ('Trim', Trim),
        ('ManufactureYear', ManufactureYear),
        ('FuelOption', FuelOption),
        ('Color', Color),
        ('InnerColor', InnerColor),
        ('EngineType', EngineType),
        ('DriveTerrain', DriveTerrain),
        ('VAS', Vas),
        ('State', State),
        ('Town', Town),
        ('Condition', Condition),
    ]
    
    user_permissions = request.user.get_all_permissions()
    allowed_models = []
    
    for name, model in models_to_manage:
        # Check for change/add permissions on the model
        has_permission = any(
            f'myapp.change_{model.__name__.lower()}' in user_permissions or
            f'myapp.add_{model.__name__.lower()}' in user_permissions
        )
        if has_permission:
            allowed_models.append({'name': name, 'model_name': model.__name__})
    
    context = {
        'unconfirmed_dealers': unconfirmed_dealers,
        'rejected_dealers': rejected_dealers,
        'approved_dealers': approved_dealers,
        'allowed_models': allowed_models,
    }
    return render(request, 'myapp/operations.html', context)

@login_required
@permission_required('myapp.change_dealerprofile', raise_exception=True)
def approve_dealer(request, pk):
    """Approves a dealer and sets their is_seller status to True."""
    if request.method == 'POST':
        try:
            dealer_profile = DealerProfile.objects.get(pk=pk)
            dealer_profile.is_confirmed = True
            dealer_profile.user.is_seller = True
            dealer_profile.user.save()
            dealer_profile.save()
            messages.success(request, f"Dealer {dealer_profile.user.username} has been approved.")
            return HttpResponseRedirect(reverse('operations'))
        except DealerProfile.DoesNotExist:
            messages.error(request, "Dealer profile not found.")
            return HttpResponseRedirect(reverse('operations'))
    return HttpResponse('Invalid request', status=400)

@login_required
@permission_required('myapp.change_dealerprofile', raise_exception=True)
def reject_dealer(request, pk):
    """Rejects a dealer's registration request."""
    if request.method == 'POST':
        try:
            dealer_profile = DealerProfile.objects.get(pk=pk)
            dealer_profile.is_rejected = True
            dealer_profile.save()
            messages.info(request, f"Dealer {dealer_profile.user.username}'s request has been rejected.")
            return HttpResponseRedirect(reverse('operations'))
        except DealerProfile.DoesNotExist:
            messages.error(request, "Dealer profile not found.")
            return HttpResponseRedirect(reverse('operations'))
    return HttpResponse('Invalid request', status=400)

@login_required
def handle_admin_tool_form(request, model_name):
    """
    Handles form submission for creating/modifying models.
    """
    model_map = {
        'Category': Category,
        'Brand': Brand,
        'VehicleModel': VehicleModel,
        'Trim': Trim,
        'ManufactureYear': ManufactureYear,
        'FuelOption': FuelOption,
        'Color': Color,
        'InnerColor': InnerColor,
        'EngineType': EngineType,
        'DriveTerrain': DriveTerrain,
        'VAS': Vas,
        'State': State,
        'Town': Town,
        'Condition': Condition,
    }

    model = model_map.get(model_name)
    if not model:
        return HttpResponse("Model not found.", status=404)

    if not request.user.has_perm(f'myapp.add_{model.__name__.lower()}') and \
       not request.user.has_perm(f'myapp.change_{model.__name__.lower()}'):
        return HttpResponse('You do not have permission to perform this action.', status=403)

    if request.method == 'POST':
        form = AdminToolForm(model, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{model_name} added/updated successfully.")
            return HttpResponseRedirect(reverse('operations'))
        else:
            html = render_to_string('myapp/partials/_admin_tools_forms.html', {'form': form, 'model_name': model_name}, request=request)
            return HttpResponse(html)
    
    form = AdminToolForm(model)
    html = render_to_string('myapp/partials/_admin_tools_forms.html', {'form': form, 'model_name': model_name}, request=request)
    return HttpResponse(html)




import requests

def fetch_vehicle_image(vin, image_size):
    url = "https://zylalabs.com/api/9168/vin+image+capture+for+vehicles+api/16576/get+image"
    params = {
        "vin": vin,
        "image size": image_size
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()  # or response.content if it's an image
    else:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")
    

from django.http import JsonResponse
from django.views import View

class VehicleImageView(View):
    def get(self, request):
        vin = request.GET.get("vin")
        image_size = request.GET.get("image_size")

        if not vin or not image_size:
            return JsonResponse({"error": "Missing vin or image_size"}, status=400)

        try:
            image_data = fetch_vehicle_image(vin, image_size)
            return JsonResponse(image_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
# views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class VINImageSearchView(APIView):
    def get(self, request):
        vin = request.query_params.get("vin")
        image_size = 300  # Hardcoded default

        if not vin:
            return Response({"error": "VIN is required."}, status=status.HTTP_400_BAD_REQUEST)

        # External API call
        url = "https://zylalabs.com/api/9168/vin+image+capture+for+vehicles+api/16576/get+image"
        params = {
            "vin": vin,
            "image size": image_size
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract and format response
            formatted = {
                "vin": vin,
                "image_url": data.get("image_url"),  # Adjust key based on actual response
                "details": data.get("text", "No details provided")  # Adjust key as needed
            }

            return Response(formatted, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        


from django.http import JsonResponse
import requests

def VINImageDrive(request, vin):
    image_size = 300

    if not vin:
        return JsonResponse({"error": "VIN is required."}, status=400)

    url = "https://zylalabs.com/api/9168/vin+image+capture+for+vehicles+api/16576/get+image"
    params = {
        "vin": vin,
        "image size": image_size
    }


    headers = {
        "Authorization": "Bearer YOUR_API_KEY"
    }


    try:
        # response = requests.get(url, params=params)
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        formatted = {
            "vin": vin,
            "image_url": data.get("image_url"),
            "details": data.get("text", "No details provided")
        }

        return JsonResponse(formatted, status=200)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=502)