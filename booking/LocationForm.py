from django import forms
from .models import Location, Seat
from django.db import transaction

class LocationUpdateForm(forms.ModelForm):
    increment_seat = forms.IntegerField(label='Increase No. of Seats', required=False, initial=0)
    existing_Seat = forms.IntegerField(label='Existing Seats', required=False, disabled=True)
    location_name = forms.CharField(label='Library Name', required=False)
    discription = forms.Textarea()
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('exposed', 'Exposed'),
    ]
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    # exclude = ()
    class Meta:
        model = Location
        fields = ['location_name','existing_Seat','increment_seat','status','discription']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial value of existing_copies from the instance
        if self.instance.pk:
            self.fields['existing_Seat'].initial = self.instance.number_of_seats
    @transaction.atomic
    def save(self, commit=True):
        if self.instance.pk:
            try:
                with transaction.atomic():
                    Location = super().save(commit=False)
                    increment = self.cleaned_data.get('increment_seat', 0)
                    print("2-------------------------------")
                    # Adjust total copies
                    if increment:
                        Location.number_of_seats += increment
                        seats = []
                        i = self.instance.number_of_seats
                        for _ in range(increment):
                            seats.append(Seat(seat_no = i,location=Location, status='vacant',created_by=Location.created_by))
                            i+=1
                        Seat.objects.bulk_create(seats)
                    print("3-------------------------------")
                    if commit:
                        Location.save()
                    return Location
            except Exception as e:
                print("Error..",e)


class LocationCreateForm(forms.ModelForm):
    pass