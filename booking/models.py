import os
from typing import Any
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone as tz
from django.core.validators import MinValueValidator,MaxLengthValidator,MinLengthValidator
from  datetime import time,timedelta
from dateutil.relativedelta import relativedelta
from customAdmin.models import CustomUser
from students.models import Student
# import calendar
from .paymentModel import Payment
class Location(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('exposed', 'Exposed'),
        # ('suspended', 'Suspended'),
    ]
    timming = [ (4,"4:00 AM Morning"), (5,"5:00 AM Morning"), (6,"6:00 AM Morning"), 
                       (7,"7:00 AM"), (8,"8:00 AM"), (9,"9:00 AM"), (10,"10:00 AM"), 
                       (11,"11:00 AM"), (12,"12:00 PM (noon)"), (13,"1:00 PM"), (14,"2:00 PM"), 
                       (15,"3:00 PM"), (16,"4:00 PM"), (17,"5:00 PM"), (18,"6:00 PM"), 
                       (19,"7:00 PM"), (20,"8:00 PM Night"), (21,"9:00 PM Night"), (22,"10:00 PM Night"), 
                       (23,"11:00 PM Night)]"),(0,	"12:00 AM, midnight Night"), (1,"1:00 AM Night"), (2,"2:00 AM Night"), 
                       (3,"3:00 AM Night"),]
    location_id = models.AutoField(primary_key=True, verbose_name="Library Id")
    location_name = models.CharField(max_length=100,verbose_name="Library Name")
    opening_time = models.PositiveIntegerField(choices=timming,verbose_name="Opening Time(leave it blank for full time)",null=True,blank=True)
    closing_time = models.PositiveIntegerField(choices=timming,verbose_name="Closing Time(leave it blank for full time)",null=True,blank=True)
    discription = models.TextField(null=True,blank=True)
    number_of_seats = models.PositiveIntegerField(verbose_name='No of Seats')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL ,null= True,blank=False,editable=False)
    class Meta:
        verbose_name = "library"          # Singular form
        verbose_name_plural = "libraries"  # Plural form
    
    def getTotalOpenTime(self):
        closing = self.closing_time
        opening = self.opening_time
        totalTime = 0
        # print(self.opening_time,self.closing_time)
        if closing and opening:
            # print(self.opening_time,self.closing_time,"innnnnn")
            i = opening
            while(i<closing):
                totalTime+=1
                # print(i,"before 24")
                i+=1
                if i>=24:
                    # print(i,"more then 24")
                    i = i%24
        # print(totalTime)
        return totalTime

    def __str__(self):
        return f'{self.location_name}-{self.location_id}'
    @transaction.atomic
    def save(self, *args, **kwargs):
        # Check if this is a new location by verifying if location_id is None
        try:
            with transaction.atomic():
        # Create seats only when a new location is created
                num_of_seat = self.number_of_seats
                if self.location_id is None:
                    super().save(*args, **kwargs)  # Save the location first to ensure it has an ID
                    seats = []
                    i = 1
                    for _ in range(num_of_seat):
                        seats.append(Seat(seat_no = i,location=self, status='vacant',created_by=self.created_by))
                        i+=1
                    Seat.objects.bulk_create(seats)
                super().save(*args, **kwargs)
        except Exception as e:
            print("Error..",e)

@receiver(post_delete, sender=Location)
def update_location_on_seat_delete(sender, instance, **kwargs):
    Seat.objects.filter(location=instance).delete()

class Seat(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('removed', 'Removed'),
    ]

    seat_id = models.AutoField(primary_key=True, verbose_name="Seat Id")
    seat_no = models.PositiveIntegerField(blank=True,null=True, verbose_name="Seat No",editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Location no.',related_name='seats')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='vacant')
    deleted = models.BooleanField(default=False,blank=None,null=False,editable=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,editable=False)
    class Meta:
        verbose_name = "Seat"          # Singular form
        verbose_name_plural = "Seats"  # Plural form

    def save(self, *args, **kwargs):
        # Check if this is a new location by verifying if location_id is None
        force_insert = kwargs.pop('force_insert', False)
        force_update = kwargs.pop('force_update', False)
        is_new = self.pk is None
        # super().save(self, *args, **kwargs)
        if is_new:
           self.seat_no = Seat.objects.filter(location=self.location).count()+ 1
           
        super().save(force_insert=force_insert, force_update=force_update, *args, **kwargs)

        if is_new:
            self.location.number_of_seats= self.location.number_of_seats + 1
            self.location.save()

    def __str__(self):
        # print(self.bookings.count())
        return 'Seat no.' +str(self.seat_no)
    def filter_available(self,joining_date,hours,total_duration):
        # filter_available_ac_j_h_dt_d(joining_date,hour,duration*multiple*type[planing_for])
        """
        Filter the start and end time options based on already booked slots for the seat.
        """
        # Get existing bookings for this seat
        # booked_slots = Booking.objects.filter(seat=self)
        # joining_date
        booked_slots = self.bookings.all()

        # Get all full hours from 00:00 to 23:00
        all_hours = [time(hour=h) for h in range(24)]  # Generates times like 00:00:00, 01:00:00, ..., 23:00:00

        # print(joining_date,hours,total_duration)
        given_date = tz.datetime.strptime(joining_date, "%Y-%m-%d")
        # Initialize the list for storing unavailable hours
        unavailable_hours = set()

        # Mark unavailable hours based on existing bookings
        for booking in booked_slots:
            daystep = given_date
            for i in range(0,total_duration):
                daystep = daystep + timedelta(days=1)
                # booked_slots.payments
                # c2 -------------  c1
                condtion1 = daystep > booking.extended_date and daystep > booking.joining_date
                condtion2 = daystep < booking.extended_date and daystep < booking.joining_date
                if not condtion1 and not condtion2 :
                    start_hour = booking.start_time.hour
                    end_hour = booking.end_time.hour
                    # Mark all hours between the start and end times as unavailable
                    unavailable_hours.update(range(start_hour+1, end_hour))  # Include all hours between start and end
        # Filter out unavailable hours to get the available ones
        # print(all_hours)
        # print(unavailable_hours)
        available_hours = [hour for hour in all_hours if hour.hour not in unavailable_hours]
        available_choices = [hour.hour for hour in available_hours]
        return {"timming":available_choices}

@receiver(post_delete, sender=Seat)
def update_location_on_seat_delete(sender, instance, **kwargs):
    location = instance.location
    location.number_of_seats -= 1
    location.save()


class Booking(models.Model):
    location = None
    plan = ""
    discount = None
    total_amount_to_pay = 0
    duration = 0
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    student = models.ForeignKey(Student,on_delete=models.PROTECT , related_name='bookings') # getting
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE,related_name='bookings') # getiing
    booking_time = models.DateTimeField(auto_now_add=True) # no issue
    extended_date = models.DateTimeField(null=True,blank=True) # solved
    joining_date = models.DateTimeField(null=True,blank=True) # getting
    start_time = models.TimeField() # getting
    end_time = models.TimeField() # getting
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active',blank=False,null=False,editable=False) # no issue
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,editable=False) # no issue
    class Meta:
        verbose_name = "Seat Booking"          # Singular form
        verbose_name_plural = "Seat Bookings"  # Plural form
    @transaction.atomic
    def save(self, *args, **kwargs) -> None:
        seat = self.seat
        student = self.student
        student.status = 'alloted'
        seat.status = 'engaged'
        print("heiiiiiiiiiiiii")
        splited_plan = self.plan.split("_")
        if splited_plan[2]=="d":
            delta = relativedelta(days=int(splited_plan[3])*self.duration)
        if splited_plan[2]=="w":
            delta = relativedelta(weeks=int(splited_plan[3])*self.duration)
        if splited_plan[2]=="m":
            delta = relativedelta(months=int(splited_plan[3])*self.duration)
        else :
            delta = relativedelta(days=0)

        self.extended_date = self.joining_date +delta
# {'student': <Student: Samarjeet Singh Gautam (enrolled)>, 'location': <Location: studento-2>, 
# 'joining_date': datetime.date(2024, 9, 17), 'plan': '6_600_m_1', 'duration': 1, 'seat_finder': '', 
# 'seat': <Seat: Seat no.4>, 'start_time': '09:00:00', 'end_time': '15:00:00', 'discount': 0.0, 'total_amount': 600.0}
        amount = int(self.plan.split("_")[1]) * self.duration
        # print(self.pk,"pk here 156" ,self.pk is None,self.pk==None)
        if self.pk is None:
            try:
                with transaction.atomic():
                    # print("hello")
                    seat.save()
                    student.save()
                    
                    payment = Payment.objects.create(
                        payment_type = "seat_book",
                        creditorstudent = self.student, # credituser or creditorstudent
                        debitoruser= self.created_by,
                    #  razorpay_payment_id razorpay_order_id razorpay_signature 
                        amount = amount,
                        paid_amount = self.total_amount_to_pay,
                        discount = self.discount,
                        status = "success"
                    )
                    super().save(*args, **kwargs)
                    BookingPayment.objects.create(
                        booking=self,
                        payment=payment
                    )
            except Exception as e:
                print("Error.." ,e)
        # super().save(*args, **kwargs)
    def __str__(self):
        return f'name: {self.student.first_name} {self.student.last_name}  Library:{self.seat.location.location_id} - seat no: {self.seat.seat_id} - ({self.status})'
class BookingPayment(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name="booking_payments")  # Reference to Booking
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,related_name="bookings")  # Reference to Payment

@receiver(post_delete,sender=Booking)
@transaction.atomic
def update_seat_on_delete_booking(sender, instance:Booking, **kwargs):
    student = instance.student
    student.status = 'enrolled' 
    try:
        with transaction.atomic():
            # print(seat.seat_id,student.phone_no,"updated succesfully")
            seat = instance.seat
            # ager sea
            if Booking.objects.filter(seat=seat).count()==0:
                seat.status = 'vacant'
                seat.save()
            student.save()
 
        # print("updated succesfully")
    except Exception as e:
        print("Error..")



class MonthlyPlan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        # ('suspended', 'Suspended'),
    ]
    planing_for_CHOICES = [
                     ('d','DAYS'),
                     ('w','WEEKS'),
                     ('m','MONTHS'),
                     ]
    timming_id = models.AutoField(primary_key=True, verbose_name="Location No")
    hours = models.PositiveIntegerField(verbose_name='No. of hours',validators=[MinValueValidator(1)])
    planing_for = models.CharField(max_length=10, choices=planing_for_CHOICES, default='m')
    duration = models.PositiveIntegerField(default=1,verbose_name="Duration (no. Days/Months/Weeks)")
    prize = models.PositiveIntegerField(verbose_name='Price(in rupees)')
    discription = models.TextField(null =True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active',editable=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL ,null= True,blank=False,editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hours', 'planing_for', 'duration', 'prize'], name='unique_plan')
        ]

    def __str__(self):
        return f'cost {self.prize} 1 month in rupee{self.prize}'
    class Meta:
        verbose_name = "Monthly Plan"          # Singular form
        verbose_name_plural = "Monthly Plans"  # Plural form

