from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import Student
from .authserializers import StudentRegistrationSerializer, LoginSerializer
from .student_form import StudentForm
class RegisterAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("yaha tak error nahi hui")
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

def get_student(request):
    student =  Student.objects.all()
    return render(request,'customadmin/students.html',{"data":student})

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student')  # Redirect to a success page
    else:
        form = StudentForm()    
    return render(request, "customadmin/student_form.html", {"form": form})
