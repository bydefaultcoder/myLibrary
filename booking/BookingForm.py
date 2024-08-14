from django import forms
from .models import Booking, Seat, Location
from .models import Booking, Seat, Location, Student

class CustomBookingForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, label='Location')

    class Meta:
        model = Booking
        fields = ['student', 'location', 'seat', 'status', 'duration' ,'start_time','end_time']

    def __init__(self, *args, **kwargs):
        # Extract the request object from kwargs
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Filter locations by the current user
        self.fields['student'].queryset = Student.objects.filter(status='inrolled')

        if self.request:
            self.fields['location'].queryset = Location.objects.filter(created_by=self.request.user)
        else:
            self.fields['location'].queryset = Location.objects.none()

        # Filter seats based on the selected location
        print('location' in self.data,self.instance.pk,"jjjjjjjj")
        if 'location' in self.data:
            try:
                location_id = int(self.data.get('location'))
                self.fields['seat'].queryset = Seat.objects.filter(status='vacant',location_id=location_id)
            except (ValueError, TypeError):
                self.fields['seat'].queryset = Seat.objects.none()
        elif self.instance.pk:
            self.fields['seat'].queryset = self.instance.location.seat_set.filter(status='vacant')
            # print(self.fields['seat'],"hello")
