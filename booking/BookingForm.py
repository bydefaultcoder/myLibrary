from django import forms
from .models import Booking, MonthlyPlan, Seat, Location
from .models import Booking, Seat, Location, Student
from datetime import time
from django import forms
from .models import Booking, Seat, Location, Student
from django.contrib.auth.hashers import check_password
from django.utils.safestring import mark_safe
from django.utils import timezone as tz
import logging
logger = logging.getLogger(__name__)
class CustomBookingForm(forms.ModelForm):
    # Define the choices for full-hour time (from 00:00 to 23:00)
    HOUR_CHOICES = [(time(hour=i).strftime('%H:%M:%S'), time(hour=i).strftime('%I %p').lstrip('0')) 
    for i in range(24)]

    # Start time and end time restricted to full-hour choices
    start_time = forms.ChoiceField(choices=HOUR_CHOICES, label="Start Time")
    end_time = forms.ChoiceField(choices=HOUR_CHOICES, label="End Time")
    # hour_duratios =  [(0,'Custom Time')] + [(i,i) for i in [4,6,8,12,24]]

    joining_date = forms.DateField(initial=tz.now())
    remain_no_of_months = forms.IntegerField(min_value=1,initial=0)
    
    plan = forms.ChoiceField(choices= [],label="Plans",)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, label='Location')
    discount= forms.FloatField(min_value=0, label='Discount in %',max_value=99)
    total_amount = forms.FloatField(min_value=1,required=True, label='Total Amount(₹)')
    # student = forms.ModelChoiceField(queryset=Student.objects.all(), required=False, label='student')
    class Meta:
        model = Booking
        fields = ['student', 'location', 'seat', 'plan','start_time', 'end_time','remain_no_of_months','discount','joining_date' ]

    def get_monthly_plans(self):
       
       plans = MonthlyPlan.objects.filter(created_by=self.request.user)
       plans_to_return = []
       for i in plans:
           plans_to_return.append((f'{i.hours}_{i.prize}',f'{i.hours} hours - monthly {i.prize}(₹)'))
       return plans_to_return


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(status='enrolled',created_by=self.request.user)
        self.fields['plan'].choices = self.get_monthly_plans()
        self.fields['total_amount'].help_text =  mark_safe(
            '<button type="button" id="total_amount_type" style= "background-color:#264b5d;color:#eeeeee;margin-left:10px;">Click to pay custom amount</button>'
        )
        if self.request:
            self.fields['location'].queryset = Location.objects.filter(created_by=self.request.user)
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
        self.fields['start_time'].choices = self.HOUR_CHOICES
        self.fields['end_time'].choices = self.HOUR_CHOICES
        self.fields['remain_no_of_months'].initial = 1
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data,"come heredm,.jsdklfjlsadk;")
        # cleaned_data
        logging.debug("clean data",cleaned_data)
        return cleaned_data
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Only allow updates to specific fields
        if obj:  # obj will be None when creating a new object
            form.base_fields = {
                key: form.base_fields[key] 
                for key in ['start_time']  # Specify fields you want to allow
            }
        
        return form


