from django import forms
from .models import Vehicle, DealerProfile, InnerColor

class VehicleForm1(forms.ModelForm):
    """
    A form for editing a vehicle's details.
    Assumes the Vehicle model has fields like brand, vehicle_model, etc.
    """
    class Meta:
        model = Vehicle
        fields = [
            'brand', 'vehicle_model', 'trim', 'manufacture_year',
            'condition', 'mileage', 'engine_type', 'fuel_option',
            'transmission', 'drive_terrain', 'color', 'inner_color','price',
            'description', 'is_available', 'image', 'number_of_view'
        ]

    # Customize widget for better user experience
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control rounded-lg'
            })
        self.fields['description'].widget.attrs.update({'rows': 4})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check-input'})



class DealerRegistrationForm(forms.ModelForm):
    """
    A form for new dealer registration.
    """
    class Meta:
        model = DealerProfile
        fields = ['business_logo', 'business_address', 'state', 'town']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control rounded-lg'
            })
        
        # Dynamically filter the towns based on the initial state
        # This is for pre-populating on GET request
        if 'state' in self.initial:
            state_id = self.initial['state']
            self.fields['town'].queryset = Town.objects.filter(state_id=state_id).order_by('name')
        else:
            self.fields['town'].queryset = Town.objects.none()
