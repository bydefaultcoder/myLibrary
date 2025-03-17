from django import forms
from ..models import Seat

class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat  # Use your model here
        fields = ['location','status']
        widgets = {
            'location': forms.Select(attrs={"autocomplete":"off"}),
            'status': forms.Select(attrs={"autocomplete":"off"}),
        }
