
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
class Payment(models.Model):
    
    # booking = models.ForeignKey(Booking, on_delete=models.CASCADE,related_name='payments')
    TYPE_CHAOICES = [("seat_book","Seat Bookijng"),
                     ("user_pay","User Payement"),
                     ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    payment_id = models.AutoField(primary_key=True, verbose_name="Location No")
    payment_type = models.CharField(choices=TYPE_CHAOICES,null=False,blank=False,verbose_name="Type Of Payment",max_length=10)
 
    # creditorstudent = models.ForeignKey(Student,null=True,on_delete=models.PROTECT,blank=True, related_name='student_payments')
    creditoruser = models.ForeignKey(CustomUser,on_delete=models.PROTECT,null=True,blank=True, related_name='creditor_payments')
    debitoruser = models.ForeignKey(CustomUser,on_delete=models.PROTECT,null=True,blank=True, related_name='debitor_payments')
    # for razorpay
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    # Payment amount and currency
    amount = models.DecimalField(decimal_places=2,max_digits=6,verbose_name='Amount (₹)',validators=[MinValueValidator(1)])
    paid_amount = models.DecimalField(max_digits=6, decimal_places=2 ,verbose_name="Amount to be paid")  # Example: 1000.00
    discount = models.DecimalField(decimal_places=2,max_digits=6,verbose_name='Discount (in %)',validators=[MinValueValidator(100)])
    currency = models.CharField(max_length=3, default='INR')  # Assuming INR for Indian Rupees
    payment_time = models.DateTimeField(auto_now_add=True)

    # Status of the payment
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def save(self, *args, **kwargs) -> None:
        print("Payment Saved")
        return super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Payment"          # Singular form
        verbose_name_plural = "Payments"  # Plural form

    def __str__(self):
        return f'{self.payment_id},paidamount:{self.amount}'
    
