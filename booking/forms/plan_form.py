from django import forms
from ..models import MonthlyPlan


class MonthlyPlanForm(forms.ModelForm):
    class Meta:
        model = MonthlyPlan
        fields = ['hours', 'planing_for', 'duration', 'prize', 'discription']

        widgets = {
            'hours': forms.NumberInput(attrs={ 'min': 4, 'placeholder': 'Enter hours'}),
            'planing_for': forms.Select(attrs={}),
            'duration': forms.NumberInput(attrs={ 'min': 1, 'placeholder': 'Enter duration'}),
            'prize': forms.NumberInput(attrs={ 'placeholder': 'Enter price in rupees'}),
            'discription': forms.Textarea(attrs={ 'rows': 3, 'placeholder': 'Enter description'}),
            # 'status': forms.Select(attrs={ 'readonly': True}),  # Readonly status
        }
