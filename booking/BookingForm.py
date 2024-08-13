from django import forms
# from booking.models import Booking, Seat, Location
# from models import Booking,Seat,Location
from .models import Booking,Seat,Location

class CustomBookingForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, label='Location')

    class Meta:
        model = Booking
        fields = ['student', 'location', 'seat', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the current user from the kwargs
        super().__init__(*args, **kwargs)
        print(user,"here")
        print(self.data.keys,"here")

        # Filter locations by the user who created them
        if user:
            self.fields['location'].queryset = Location.objects.filter(created_by=user)
        else:
            self.fields['location'].queryset = Location.objects.none()
            
        if 'location' in self.data:
            try:
                location_id = int(self.data.get('location'))
                self.fields['seat'].queryset = Seat.objects.filter(location_id=location_id)
            except (ValueError, TypeError):
                self.fields['seat'].queryset = Seat.objects.none()
        elif self.instance.pk:
            self.fields['seat'].queryset = self.instance.location.seat_set.all()
