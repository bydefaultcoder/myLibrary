from django import forms
from ..models import Location

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Location  # Use your model here
        fields = ['location_name', 'number_of_seats', 'timming', 'opening_time', 'closing_time','discription']
        
        widgets = {
            'location_name': forms.TextInput(attrs={"autocomplete":"off"}),
            'number_of_seats': forms.NumberInput(attrs={"autocomplete":"off"}),
            'timming': forms.Select(attrs={"autocomplete":"off"}),
            'opening_time': forms.Select(attrs={"autocomplete":"off"}),
            'closing_time': forms.Select(attrs={"autocomplete":"off"}),
            'discription': forms.Textarea(attrs={"autocomplete":"off", 'rows': 100}),
        }
