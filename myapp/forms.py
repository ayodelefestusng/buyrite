# forms.py
from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

# myapp/forms.py
from django import forms
from .models import (
    Vehicle, Brand, VehicleModel, Trim, ManufactureYear, Condition,
    FuelOption, Color, EngineType, DriveTerrain, State, Town, Vas, User
)

class VehicleForm(forms.ModelForm):
    # Initial empty querysets for dynamic fields
    # HTMX will update these fields
    vehicle_model = forms.ModelChoiceField(
        queryset=VehicleModel.objects.none(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'hx-get': '/load_trims/', # URL for HTMX endpoint
            'hx-trigger': 'change',
            'hx-target': '#div_id_trim', # Target the div containing the trim field
            'hx-swap': 'outerHTML',
            'name': 'vehicle_model' # Ensure the name attribute is correct for the HTMX request
        })
    )
    trim = forms.ModelChoiceField(
        queryset=Trim.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    town = forms.ModelChoiceField(
        queryset=Town.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Vehicle
        # Exclude 'seller' as it will be set by the view
        # Exclude metadata fields that are auto-generated
        exclude = ['seller', 'slug', 'index', 'created_at', 'date_sold', 'number_of_view', 'vin']
        
        widgets = {
            'brand': forms.Select(attrs={
                'class': 'form-select',
                'hx-get': '/load_models/', # URL for HTMX endpoint
                'hx-trigger': 'change',
                'hx-target': '#div_id_vehicle_model', # Target the div containing the model field
                'hx-swap': 'outerHTML',
                'name': 'brand' # Ensure the name attribute is correct for the HTMX request
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'manufacture_year': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'fuel_option': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'engine_type': forms.Select(attrs={'class': 'form-select'}),
            'drive_terrain': forms.Select(attrs={'class': 'form-select'}),
            'state': forms.Select(attrs={
                'class': 'form-select',
                'hx-get': '/load_towns/', # URL for HTMX endpoint
                'hx-trigger': 'change',
                'hx-target': '#div_id_town', # Target the div containing the town field
                'hx-swap': 'outerHTML',
                'name': 'state' # Ensure the name attribute is correct for the HTMX request
            }),
            'exchange_option': forms.Select(attrs={'class': 'form-select'}),
            'registered': forms.Select(attrs={'class': 'form-select'}),
            'negotiable': forms.Select(attrs={'class': 'form-select'}),
            'no_of_tyres': forms.NumberInput(attrs={'class': 'form-control'}),
            'seat': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'number_cylinder': forms.NumberInput(attrs={'class': 'form-control'}),
            'horsepower': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'social_media': forms.URLInput(attrs={'class': 'form-control'}),
            'vas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input ms-2'}), # Adjusted class for spacing
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image6': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image7': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image8': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image9': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image10': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize querysets for dynamic fields based on existing data if the form is bound (e.g., for editing)
        if 'brand' in self.data: # Check if data is present in POST
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['vehicle_model'].queryset = VehicleModel.objects.filter(brand_id=brand_id).order_by('name')
            except (ValueError, TypeError):
                pass # Invalid input, leave queryset empty
        elif self.instance.pk and self.instance.brand: # For existing instances
            self.fields['vehicle_model'].queryset = VehicleModel.objects.filter(brand=self.instance.brand).order_by('name')

        if 'vehicle_model' in self.data:
            try:
                model_id = int(self.data.get('vehicle_model'))
                self.fields['trim'].queryset = Trim.objects.filter(vehicle_model_id=model_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.vehicle_model:
            self.fields['trim'].queryset = Trim.objects.filter(vehicle_model=self.instance.vehicle_model).order_by('name')

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['town'].queryset = Town.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.state:
            self.fields['town'].queryset = Town.objects.filter(state=self.instance.state).order_by('name')

        # Add Bootstrap classes to all fields (crispy forms handles most, but for explicit control)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple)):
                current_classes = field.widget.attrs.get('class', '')
                if 'form-control' not in current_classes and 'form-select' not in current_classes:
                     # Add form-control for text inputs, number inputs, etc.
                    field.widget.attrs['class'] = current_classes + (' form-control' if 'select' not in field.widget.__class__.__name__.lower() else '')
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                # Crispy Forms renders CheckboxSelectMultiple as a list of inputs; this class applies to individual inputs
                pass # The widget in Meta already handles this for 'vas'