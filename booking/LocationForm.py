from django import forms
from .models import Location, Seat
from django.db import transaction
from django.core.exceptions import ValidationError
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
        fields = ['location_name','existing_Seat','opening_time','closing_time','increment_seat','status','discription']
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
    def clean(self):
        cleaned_data = super().clean()
        # Fetching opening and closing times from the form data
        opening_time = cleaned_data.get("opening_time")
        closing_time = cleaned_data.get("closing_time")
        # Check if both fields are empty or one is empty
        # del cleaned_data['opening_time']  # it is to remove field before sending to save
        if (opening_time or not closing_time) and (not opening_time or closing_time):
            return cleaned_data
        else:
            raise ValidationError("Both opening and closing times both must be Fill or None of both.")


           

    # class Meta:
    #     model = Location
    #     fields = ['location_name','opening_time','closing_time','number_of_seats','status','discription']