from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from customAdmin.models import CustomUser
from .models import Student
from .Serializers.StudentSerializers import StudentRegistrationSerializer, LoginSerializer
from .student_form import StudentForm
from django.contrib.auth.models import Group
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = StudentRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save user and explicitly retrieve it
        try:
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "message": "Student registered successfully!"
            }, status=status.HTTP_201_CREATED)
        except:
            return Response({
                "message": "Server Error!"
            }, status=status.HTTP_502_BAD_GATEWAY)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

def get_student(request):
    print(request.user.pk,"given user")
    """Get students for Vendor Staff including Vendor and sibling Vendor Staff."""
    if request.user.groups.filter(name="Vendor Staff").exists():
        # Get the vendor who created this staff
        vendor = CustomUser.objects.filter(groups__name="Vendor", students=request.user).first()
        if vendor:
            # Get all Vendor Staff under the same Vendor
            vendor_staff = CustomUser.objects.filter(created_by=vendor)
            # Fetch students created by Vendor and their Vendor Staff
            student = Student.objects.filter(created_by__in=[vendor] | vendor_staff)
        else:
            student =  Student.objects.all().filter(created_by=request.user)
    else :
        student =  Student.objects.all().filter(created_by=request.user)

    return render(request,'vender/students.html',{"data":student})



def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            qr = form.save(commit=False)
            qr.created_by = request.user  # Set the creator
            qr.save()
            return redirect('student')  # Redirect to a success page
    else:
        form = StudentForm()    
    return render(request, "vender/student_form.html", {"form": form})
