from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'avatar',
            'c_number',
            'w_number',
            'fullname', 
            'address',
            ]
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'c_number': forms.TextInput(attrs={'class': 'form-control'}),
            'w_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            if avatar.size > 10485760:  # 10 MB
                raise forms.ValidationError("The maximum file size that can be uploaded is 10MB")
        return avatar
