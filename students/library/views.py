from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from booking.models import Location
from .libratyserializers import LocationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# from .authserializers import StudentRegistrationSerializer, LoginSerializer

class LocationAPIView(generics.ListAPIView):
    queryset = Location.objects.filter(status="exposed")  # Fetch all books from the database
    serializer_class = LocationSerializer  # Use this serializer to transform the data into JSON
        # Apply TokenAuthentication and IsAuthenticated permission to the view
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
