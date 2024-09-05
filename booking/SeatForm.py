from django import forms
from .models import Booking, Seat

class SeatForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('removed', 'Removed'),
    ]


    class Meta:
        model = Seat
        fields = ['title', 'author', 'status', 'existing_copies', 'increment_copies', 'decrement_copies']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Check if this form is for an existing instance (update) or new instance (create)
        if self.instance.pk:
            # self.fields['status'].choices = self.STATUS_CHOICES
            if Booking.objects.exists(seat=self.instance.pk):
                self.fields['status'].choices = [ ('engaged', 'Engaged'),]
                self.fields['status'].initial = self.instance.status
        else:
            # This is a create, show create choices
            self.fields['status'].choices = self.STATUS_CHOICES
