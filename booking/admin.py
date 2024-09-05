from typing import Any
from django.contrib import admin

from .LocationForm import LocationUpdateForm,LocationCreateForm
# LocationCreateForm, 
from .filters import SeatFilterByLocations
from customAdmin.admin import CustomUserAdmin, admin_site 
from customAdmin.models import CustomUser
# from myLibrary.customAdmin.customAdminForm import CustomUserCreationForm
from .BookingForm import CustomBookingForm
from .models import MonthlyPlan, Payment, Student,Seat,Booking,Location
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Min, Max ,Count, Q
import logging
from django.utils.html import format_html
from django.utils import timezone as tz
from dateutil.relativedelta import relativedelta
import csv
from django.http import HttpResponse
logger = logging.getLogger(__name__)


admin_site.register(Group)
admin_site.register(CustomUser,CustomUserAdmin)

class LocationAdmin(admin.ModelAdmin):

    list_display = ('display_name','number_of_seats','discription',)
    def display_name(self,modelObject):
        return f"{modelObject.location_name}-({modelObject.location_id})"

    oldForm =  None
    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            self.form = LocationUpdateForm
        else:
            self.form = LocationCreateForm


        return super().get_form(request, obj, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created
            obj.created_by = request.user
        obj.save()
    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    def __init__(self, model: type, admin_site: admin.AdminSite | None) -> None:
        super().__init__(model, admin_site)

# @admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # list_display = ('Studnt_Name', 'Seat_no', 'booking_time', 'timming', 'duration',)
    list_display = ('Studnt_Name', 'Seat_no', 'booking_time', 'timming','days_to_expire')
    list_filter = ('status',)
    search_fields = ('getStuName', 'seat')
    form = CustomBookingForm

    actions = ['custom_bulk_delete']

    def timming(self,modelObject):
        return f"{self.convertToReadableTimeing(f"{modelObject.start_time}")} to {self.convertToReadableTimeing(f"{modelObject.end_time}")}"

    def days_to_expire(self,modelObject):
        objects  = Payment.objects.filter(booking=modelObject.pk)
        # currentMonthObj = None
        for obj in objects:
            print(obj.joining_date,obj.remain_no_of_months)
            commingdate = obj.joining_date + relativedelta(months=obj.remain_no_of_months)
            days_remain = commingdate - tz.now().date()
            if obj.joining_date <= tz.now().date():
               if  days_remain.days <0:
                   return "Expired"
               elif days_remain.days ==0:
                   return "Expiring today"
               else:
                   return f"{days_remain.days} days to expire"
        # commingdate = objects.latest('pk').joining_date + relativedelta(months=0)
        rem_day = objects.latest('pk').joining_date - tz.now().date() 
        return f'{rem_day.days} days to join (for {obj.remain_no_of_months} month)'
    
    def convertToReadableTimeing(self,time_str):
        t = int(time_str.split(":")[0])
        if t>=13:
            return f"{t-12} PM"
        else:
            return f"{t} AM"
    def get_form(self, request, obj=None, **kwargs):
        # Get the form class first
        form = super().get_form(request, obj, **kwargs)

        # Create a wrapper that passes the request to the form
        class CustomFormWithRequest(form):
            def __init__(self, *args, **form_kwargs):
                form_kwargs['request'] = request
                super().__init__(*args, **form_kwargs)

        return CustomFormWithRequest

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/select2@4.1.0-beta.2/dist/css/select2.min.css',
                # Include any additional CSS files here
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',  # jQuery library
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-beta.2/dist/js/select2.min.js',  # Select2 library
            'booking/js/booking_admin.js',  # Your custom JavaScript file
        )
    def Studnt_Name(self,modelObject):
        return modelObject.student.name

    def Seat_no(self,modelObject):
        return modelObject.seat.seat_no
    
    @transaction.atomic
    def custom_bulk_delete(self, request, queryset):
        selected_pks = []
        num_deleted = 0
        for booking in queryset:
            try:
                with transaction.atomic():
                    if booking.status == 'active':
                        selected_pks.append(booking.seat_id)
                        booking.delete()
                        num_deleted += 1
                    else:
                        messages.warning(request, f'{booking} cannot be deleted due to some constraints.')
            except Exception as e:
                messages.error(request, f'Error deleting {booking}: {str(e)}')

        # Notify the user about the number of objects deleted
        if num_deleted > 0:
            # selected_pks = queryset.values
            updated_count = Seat.objects.filter(pk__in=selected_pks).update(status='vacant')
            # Student.objects.filter(pk__in=selected_pks)
            self.message_user(request, _(f'{updated_count} seats were marked as inactive.'))
            self.message_user(request, _(f'Successfully deleted {num_deleted} item(s).'), messages.SUCCESS)
        else:
            self.message_user(request, _('No items were deleted.'), messages.WARNING)

    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    custom_bulk_delete.short_description = _('Delete selected items (with custom logic)')
    

    def save_model(self, request, obj, form, change):
        if form.is_valid():
        # Attach extra fields to the model instance
            obj.location = form.cleaned_data.get('location')
            obj.discount = form.cleaned_data.get('discount')
            obj.plan = form.cleaned_data.get('plan')
            obj.total_amount = form.cleaned_data.get('total_amount')
            obj.remain_no_of_months = form.cleaned_data.get('remain_no_of_months')
            # print(tz.datetime(form.cleaned_data.get('joining_date')))
            obj.joining_date = form.cleaned_data.get('joining_date')
            logger.info(msg=f"{obj} hello line no 63")
            if not change:
              obj.created_by = request.user
            return obj.save()
            # super().save_model(request, obj, form, change)
        else:
            logger.info("form is not valid")



    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'student':
            formfield.queryset = Student.objects.filter(created_by=request.user)
        if db_field.name == 'seat' :
            # Filter locations based on the current user
            formfield.queryset = Seat.objects.filter(created_by=request.user)
        return formfield


    # def save_model(self, request, obj, form, change):
    #     # Here, request.user is the currently logged-in admin
    #     if not change:  # If creating a new object
    #         obj.created_by = request.user
    #     obj.save()

# @admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    # actions = ['custom_delete']
    list_display = ('seat_no','location','start_and_end_timing')
    ordering = ('seat_no',)
    # list_filter = ('status',)
    list_filter = (SeatFilterByLocations,)  # Filter by location
    # search_fields = ('seat_no','status','location__description')  # Allows search by seat ID and location description

    class Meta:
        ordering = ['-seat_no']  # Sorts by title in ascending order

    def start_and_end_timing(self, modelObject):
        # Filter bookings for the specific seat
        if modelObject.status == 'removed':
            return "Removed"
        seatObj = Booking.objects.filter(seat=modelObject)
        # Aggregate to get the earliest start_time and the latest end_time
        start_time = seatObj.aggregate(start_time=Min('start_time'))['start_time']
        end_time = seatObj.aggregate(end_time=Max('end_time'))['end_time']

        if start_time and end_time:
            return f'{start_time} - {end_time}'
        else:
            return 'Not alloted (Active)'
        # return '333'

    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created
            # obj.seat_no = Seat.objects.filter(location=obj.location).count()+ 1
            # print("hello here is seat no" ,obj.seat_no)
            obj.created_by = request.user
        obj.save()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # print(db_field)s
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'location':
            formfield.queryset = Location.objects.filter(created_by=request.user)
        if db_field.name == 'student':
            formfield.queryset = Student.objects.filter(created_by=request.user)
        return formfield

class MonthlyPlanAdmin(admin.ModelAdmin):
    list_display = ('getPlanningFor','getHours', 'getPrize',  'status')
    list_filter = ('status','hours', 'prize','planing_for')
    search_fields = ('hours', 'phone_no')

    def getPrize(self, modelObj):
        return f'{modelObj.prize} ₹'
    getPrize.short_description = _('Prize (₹)')

    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    def getPlanningFor(self, modelObj):
        if modelObj.planing_for=="d" :
          output = f'For {modelObj.duration} Days'
        if modelObj.planing_for=="m" :
          output = f'For {modelObj.duration} Months'
        if modelObj.planing_for=="w" :
          output = f'For {modelObj.duration} Weeks'
        return output
    getPlanningFor.short_description = _('Planning For')

    def getHours(self, modelObj):
        return f'{modelObj.hours} Hours'
    getPlanningFor.short_description = _('No. OF hours')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created
            # obj.seat_no = Seat.objects.filter(location=obj.location).count()+ 1
            # print("hello here is seat no" ,obj.seat_no)
            obj.created_by = request.user
        obj.save()
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount','paid_amount','discount','payment_time')
    list_filter = ('booking','paid_amount',)
    search_fields = ('payment_time',)
    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created
            # obj.seat_no = Seat.objects.filter(location=obj.location).count()+ 1
            # print("hello here is seat no" ,obj.seat_no)
            obj.created_by = request.user
        obj.save()

admin_site.register(Payment,PaymentsAdmin)
admin_site.register(MonthlyPlan,MonthlyPlanAdmin)
admin_site.register(Seat,SeatAdmin)
admin_site.register(Location,LocationAdmin)
admin_site.register(Booking,BookingAdmin)
