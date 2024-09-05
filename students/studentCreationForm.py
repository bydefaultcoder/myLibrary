from typing import Any
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Student

class StudentCreationForm(forms.ModelForm):
    """Form for creating new users with password hashing"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Student

        fields = ('first_name','last_name','phone_no','email','avatar','adhar_no','address')  # Add your custom fields here

    # stu_no avatar  phone_no address adhar_no first_name last_name
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user