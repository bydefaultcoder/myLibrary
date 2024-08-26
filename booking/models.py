from typing import Any
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone as tz
from django.core.validators import MinValueValidator,MaxValueValidator


from customAdmin.models import CustomUser
# import calendar
 
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
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL ,null= True,blank=False,editable=False)
    class Meta:
        verbose_name = "library"          # Singular form
        verbose_name_plural = "libraries"  # Plural form

    def __str__(self):
        return f'{self.location_name}-{self.location_id}'

    def save(self, *args, **kwargs):
        # Check if this is a new location by verifying if location_id is None
        creating_new = self.location_id is None
        # Create seats only when a new location is created
        num_of_seat = self.number_of_seats
        if creating_new:
            self.number_of_seats = 0
            super().save(*args, **kwargs)  # Save the location first to ensure it has an ID
            for _ in range(num_of_seat):
                Seat.objects.create(location=self, status='vacant',created_by=self.created_by)
        super().save(*args, **kwargs)

@receiver(post_delete, sender=Location)
def update_location_on_seat_delete(sender, instance, **kwargs):
    Seat.objects.filter(location=instance).delete()

class Seat(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('engaged', 'Engaged'),
        ('inactive', 'Inactive'),
    ]
    seat_id = models.AutoField(primary_key=True, verbose_name="Seat Id")
    seat_no = models.PositiveIntegerField(blank=True,null=True, verbose_name="Seat No",editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Location no.')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='vacant')
    deleted = models.BooleanField(default=False,blank=None,null=False)
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
        return 'Seat no.' +str(self.seat_id) + ' status:' + self.status 

@receiver(post_delete, sender=Seat)
def update_location_on_seat_delete(sender, instance, **kwargs):
    location = instance.location
    location.number_of_seats -= 1
    location.save()

class Student(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('alloted', 'Alloted'),
        ('suspended', 'Suspended'),
    ]
    stu_no = models.PositiveIntegerField(blank=True,null=True,editable=False)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    adhar_no = models.CharField(max_length=12, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,editable=False)
    class Meta:
        verbose_name = "Student"          # Singular form
        verbose_name_plural = "Students"  # Plural form

    def __str__(self):
        return f"{self.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Check if the status has changed
        
        if self.pk:
            old_status = Student.objects.get(pk=self.pk).status
            if old_status == 'enrolled':
                self.status = 'alloted'
            else:
                self.status = 'enrolled'
        else:
           self.stu_no = Student.objects.filter(created_by=self.created_by).count()+ 1

        super().save(*args, **kwargs)

class Booking(models.Model):
    location = None
    plan = None
    discount = None
    total_amount = None
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    joining_date = None
    remain_no_of_months = None
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active',blank=False,null=False,editable=False)
    duration = models.DurationField( default=tz.timedelta(days=30))
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,editable=False)
    class Meta:
        verbose_name = "Seat Booking"          # Singular form
        verbose_name_plural = "Seat Bookings"  # Plural form

    def save(self, *args, **kwargs) -> None:
        seat = self.seat
        student = self.student
        student.status = 'alloted'
        seat.status = 'engaged'
        print(kwargs,args)
        print(self.student,self.seat,self.location,self.plan,self.start_time,self.end_time,self.remain_no_of_months,self.discount,self.joining_date,self.total_amount,"here")
            # {-'student': <Student: Vinay (enrolled)>, 
        amount = int(self.plan.split("_")[1]) * int(self.remain_no_of_months)
        print(self.pk,"pk here 156" ,self.pk is None,self.pk==None)
        if self.pk is None:
            try:
                with transaction.atomic():
                    print("hello")
                    seat.save()
                    student.save()
                    super().save(*args, **kwargs)
                    Payment.objects.create(booking=self,
                                           amount = amount,
                                           paid_amount=self.total_amount,
                                           discount=self.discount,
                                           joining_date = self.joining_date,
                                           remain_no_of_months = self.remain_no_of_months,
                                           created_by=self.created_by)
            except Exception as e:
                print("Error.." ,e)

    def __str__(self):
        return f'name:{self.student.name} - room/hall:{self.seat.location.location_id} - seat no: {self.seat.seat_id} - ({self.status})'

@receiver(post_delete,sender=Booking)
@transaction.atomic
def update_seat_on_delete_booking(sender, instance:Booking, **kwargs):
    student = instance.student
    student.status = 'enrolled' 
    try:
        with transaction.atomic():
            # print(seat.seat_id,student.phone_no,"updated succesfully")
            seat = instance.seat
            if Booking.objects.filter(seat=seat).count() >=1:
                seat.status = 'vacant'
                seat.save()
            student.save()
 
        # print("updated succesfully")
    except Exception as e:
        print("Error..")




    # user.
    # location = instance.location
    # location.number_of_seats -= 1
    # location.save()



class MonthlyPlan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        # ('suspended', 'Suspended'),
    ]
    timming_id = models.AutoField(primary_key=True, verbose_name="Location No")
    hours = models.PositiveIntegerField(verbose_name='No. of hours',validators=[MinValueValidator(1)])
    prize = models.PositiveIntegerField(verbose_name='Monthly price(in rupees)')
    discription = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL ,null= True,blank=False,editable=False)

    def __str__(self):
        return f'cost {self.prize} 1 month in rupee{self.prize}'
    class Meta:
        verbose_name = "Monthly Plan"          # Singular form
        verbose_name_plural = "Monthly Plans"  # Plural form


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True, verbose_name="Location No")
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,related_name='payments')
    amount = models.DecimalField( decimal_places=2,max_digits=6,verbose_name='Amount (₹)',validators=[MinValueValidator(1)])
    paid_amount = models.DecimalField( decimal_places=2,max_digits=6,verbose_name='Paid Amount (₹)',validators=[MinValueValidator(1)])
    discount = models.DecimalField(decimal_places=2,max_digits=6,verbose_name='Discount (in %)',validators=[MinValueValidator(100)])
    payment_time = models.DateTimeField(auto_now_add=True)
    joining_date = models.DateField(blank=False,null=False, verbose_name="Joining from",default=tz.now())
    remain_no_of_months = models.PositiveIntegerField(default=1,verbose_name="No. of Months",validators=[MinValueValidator(1)])
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL ,null= True,blank=False,editable=False)
    class Meta:
        verbose_name = "Payment"          # Singular form
        verbose_name_plural = "Payments"  # Plural form

    def __str__(self):
        return f'Bookingid:{self.booking.pk},{self.paid_amount},monthAdded:{self.remain_no_of_months}'