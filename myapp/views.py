from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect,
    HttpResponseServerError
)
from .models import Category,Carousel,Post
from django.utils.timezone import now

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

class HomeView(ListView):
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

