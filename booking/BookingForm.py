from django import forms
from .models import Booking, Seat, Location
from .models import Booking, Seat, Location, Student
from datetime import time
from django import forms
from .models import Booking, Seat, Location, Student
from django.contrib.auth.hashers import check_password
import datetime

class CustomBookingForm(forms.ModelForm):
    # Define the choices for full-hour time (from 00:00 to 23:00)
    HOUR_CHOICES = [(time(hour=i).strftime('%H:%M:%S'), time(hour=i).strftime('%I %p').lstrip('0')) 
    for i in range(24)]

    # Start time and end time restricted to full-hour choices
    start_time = forms.ChoiceField(choices=HOUR_CHOICES, label="Start Time")
    end_time = forms.ChoiceField(choices=HOUR_CHOICES, label="End Time")
    hour_duratios =  [(0,'Custom Time')] + [(i,i) for i in [4,6,8,12,24]]
    
    hours = forms.ChoiceField(choices= hour_duratios,label="Hours")
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, label='Location')
    class Meta:
        model = Booking
        fields = ['student', 'location', 'seat', 'status', 'hours','start_time', 'end_time', 'duration' ]


    def __init__(self, *args, **kwargs):
        # Extract the request object from kwargs to access the current user
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Filter students based on status (only enrolled students)
        print("form created...............")
        self.fields['student'].queryset = Student.objects.filter(status='enrolled')

        # Filter locations based on user-created ones if the request is available
        if self.request:
            self.fields['location'].queryset = Location.objects.filter(created_by=self.request.user)
        else:
            self.fields['location'].queryset = Location.objects.none()

        # Dynamically filter seats based on the selected location
        if 'location' in self.data:
            try:
                location_id = int(self.data.get('location'))
                self.fields['seat'].queryset = Seat.objects.filter(location_id=location_id)
            except (ValueError, TypeError):
                self.fields['seat'].queryset = Seat.objects.none()
        elif self.instance.pk:
            self.fields['seat'].queryset = self.instance.location.seat_set.all()
        self.fields['start_time'].choices = self.HOUR_CHOICES
        self.fields['end_time'].choices = self.HOUR_CHOICES
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


