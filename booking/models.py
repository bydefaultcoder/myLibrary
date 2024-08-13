from typing import Any
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, date
import calendar

class Location(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        # ('suspended', 'Suspended'),
    ]
    location_name = models.CharField(max_length=100)
    location_id = models.AutoField(primary_key=True, verbose_name="Location No")
    discription = models.TextField()
    number_of_seats = models.PositiveIntegerField(verbose_name='No of Seats')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL ,null= True,blank=False,editable=False)

    def __str__(self):
        return str(self.location_id)

    def save(self, *args, **kwargs):
        # Check if this is a new location by verifying if location_id is None
        creating_new = self.location_id is None
        # Create seats only when a new location is created
        print(self.created_by)
        super().save(*args, **kwargs)  # Save the location first to ensure it has an ID
        if creating_new:
            print(self.number_of_seats)
            for _ in range(self.number_of_seats):
                Seat.objects.create(location=self, status='vacant',created_by=self.created_by)

# class Timing

@receiver(post_delete, sender=Location)
def update_location_on_seat_delete(sender, instance, **kwargs):
    Seat.objects.filter(location=instance).delete()

class Seat(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('engaged', 'Engaged'),
        ('inactive', 'Inactive'),
    ]
    seat_id = models.AutoField(primary_key=True, verbose_name="Seat No")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Location no.')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='vacant')
    deleted = models.BooleanField(default=False,blank=None,null=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,editable=False)

    def save(self, *args, **kwargs):
        # Check if this is a new location by verifying if location_id is None
        force_insert = kwargs.pop('force_insert', False)
        force_update = kwargs.pop('force_update', False)
        is_new = self.pk is None
        # super().save(self, *args, **kwargs)
        super().save(force_insert=force_insert, force_update=force_update, *args, **kwargs)
        if is_new:
            self.location.number_of_seats +=1
            self.location.save()

    def __str__(self):
        return 'Seat no.' +str(self.seat_id) + ' status:' + self.status 

@receiver(post_delete, sender=Seat)
def update_location_on_seat_delete(sender, instance, **kwargs):
    location = instance.location
    location.number_of_seats -= 1
    location.save()

class Student(models.Model):
    STATUS_CHOICES = [
        ('inrolled', 'Inrolled'),
        ('alloted', 'Alloted'),
        ('suspended', 'Suspended'),
    ]

    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    adhar_no = models.CharField(max_length=12, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,editable=False)

    def __str__(self):
        return f"{self.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Check if the status has changed
        print("problems comes here")
        if self.pk:
            old_status = Student.objects.get(pk=self.pk).status
            if old_status == 'inrolled':
                self.status = 'alloted'
            else:
                self.status = 'Inrolled'

        super().save(*args, **kwargs)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active',blank=False,null=False)
    booking_time = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(default=timedelta(days=30))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,editable=False)

    def save(self, *args, **kwargs) -> None:
        seat = self.seat
        student = self.student

        student.status = 'alloted'
        seat.status = 'engaged'
        print(student)
        try:
            with transaction.atomic():
                # problem
                # super().save()
                seat.save()
                student.save()
                super().save(*args, **kwargs)
            print("updated succesfully")
                # print(seat.seat_id,student.phone_no,"updated succesfully")
        except Exception as e:
            print("Error.." ,e)
    def __str__(self):
        return f'name:{self.student.name} - room/hall:{self.seat.location.location_id} - seat no: {self.seat.seat_id} - ({self.status})'

@receiver(post_delete,sender=Booking)
@transaction.atomic
def update_seat_on_delete_booking(sender, instance:Booking, **kwargs):
    seat = instance.seat
    student = instance.student
    student.status = 'inrolled' 
    seat.status = 'vacant'
    try:
        with transaction.atomic():
            print(seat.seat_id,student.phone_no,"updated succesfully")
            seat.save()
            student.save()
 
        print("updated succesfully")
    except Exception as e:
        print("Error..")




    # user.
    # location = instance.location
    # location.number_of_seats -= 1
    # location.save()