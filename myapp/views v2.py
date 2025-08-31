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
    ManufactureYear, FuelOption, Color, EngineType, DriveTerrain, VAS
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

@method_decorator(login_required, name='dispatch')
class DashboardView(ListView):
    model = Vehicle
    template_name = 'myapp/dashboard.html'
    context_object_name = 'vehicles'
    
    def get_queryset(self):
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
        
        if user.is_superuser:
            queryset = Vehicle.objects.all().order_by('-created_at')
        else:
            queryset = Vehicle.objects.filter(owner=user).order_by('-created_at')

        if status == 'sold':
            queryset = queryset.filter(is_available=False)
        elif status == 'unsold':
            queryset = queryset.filter(is_available=True)
        
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
        
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['states'] = State.objects.all()
        context['trims'] = Trim.objects.all()
        context['inner_colors'] = InnerColor.objects.all()
        context['colors'] = Vehicle.objects.values_list('color', flat=True).distinct()
        
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
        
        if request.user == vehicle.owner or request.user.is_superuser:
            vehicle.is_available = False
            vehicle.save()
            return HttpResponse(status=200)
        
        return HttpResponse('Unauthorized', status=403)
    return HttpResponse('Invalid Request', status=400)


@login_required
def edit_vehicle(request, pk):
    """Handles vehicle editing via a form in a modal."""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.user != vehicle.owner and not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=403)
        
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return render(request, 'myapp/partials/_vehicle_card.html', {'vehicle': vehicle})
        else:
            return render(request, 'myapp/partials/_edit_vehicle_modal.html', {'form': form, 'vehicle': vehicle})
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, 'myapp/partials/_edit_vehicle_modal.html', {'form': form, 'vehicle': vehicle})


@login_required
def upload_vehicle(request):
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
        ('VAS', VAS),
        ('State', State),
        ('Town', Town),
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
        'VAS': VAS,
        'State': State,
        'Town': Town,
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
