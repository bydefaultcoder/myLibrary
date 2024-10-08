from rest_framework import serializers
from .models import Student
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        # fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'password']
        fields = [  
            "email",
            "first_name",
            "last_name",
            "phone_no",
            "date_of_birth",
            "password",
            "address",
            "adhar_no",]

    def create(self, validated_data):

        print(validated_data)
        user = Student.objects.create_user(
            # username=validated_data['phone_no'],  #  username is phone
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_no=validated_data['phone_no'],
            date_of_birth=validated_data['date_of_birth'],
            password=validated_data['password'],
            address=validated_data['address'],
            adhar_no=validated_data['adhar_no'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            print(email,password)
            passw = password  # Set your default password here
            user = Student.objects.get(email=email)
            print(user)
            if user:
                print(passw,"and ",user.password)
                if user.password == make_password(password):
                    if not user.is_active:
                        raise serializers.ValidationError('Account is disabled.')
                    raise serializers.ValidationError('Invalid Password.')
                return user
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
