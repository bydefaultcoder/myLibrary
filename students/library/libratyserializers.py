from rest_framework import serializers
from booking.models import Location
# class LocationSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Location  # Specify the model to serialize
    #     fields = ['location_id', 'location_name','timming','opening_time','closing_time','discription','number_of_seats']  # Specify the fields to include

class LocationSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # description = serializers.CharField(max_length=255)
    class Meta:
        model = Location  # Specify the model to serialize
        fields = ['location_id', 'location_name','timming','opening_time','closing_time','discription','number_of_seats']  # Specify the fields to include
