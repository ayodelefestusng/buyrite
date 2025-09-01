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
