from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['email','first_name', 'last_name', 'date_of_birth', 'phone_no', 'adhar_no', 'avatar']  
        
        widgets = {
            'email': forms.TextInput(attrs={'type': 'email'}),
            'first_name': forms.TextInput(attrs={"autocomplete":"off"}),
            'last_name': forms.TextInput(attrs={"autocomplete":"off"}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', "autocomplete":"off"}),
            'phone_no': forms.TextInput(attrs={"autocomplete":"off"}),
            'adhar_no': forms.TextInput(attrs={"autocomplete":"off"}),
        }

    def clean_phone_no(self):
        """ Ensure phone number is exactly 10 digits """
        phone_no = self.cleaned_data.get('phone_no')
        if len(phone_no) != 10 or not phone_no.isdigit():
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone_no

    def clean_adhar_no(self):
        """ Ensure Aadhaar number is exactly 12 digits """
        adhar_no = self.cleaned_data.get('adhar_no')
        if len(adhar_no) != 12 or not adhar_no.isdigit():
            raise forms.ValidationError("Aadhaar number must be exactly 12 digits.")
        return adhar_no