from rest_framework import serializers
from booking.models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location  # Specify the model to serialize
        fields = ['location_id', 'location_name','timming','opening_time','closing_time','discription','number_of_seats']  # Specify the fields to include
