from django.contrib import admin
from customAdmin.admin import CustomUserAdmin, admin_site
from customAdmin.models import CustomUser
# from myLibrary.customAdmin.customAdminForm import CustomUserCreationForm
from .BookingForm import CustomBookingForm
from .models import Monthly_prizing, Payments, Student,Seat,Booking,Location
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Min, Max


admin_site.register(Group)
admin_site.register(CustomUser,CustomUserAdmin)

class LocationAdmin(admin.ModelAdmin):
    # list_display
    list_display = ('display_name','number_of_seats','discription',)
    def display_name(self,modelObject):
        return f"{modelObject.location_name}-({modelObject.location_id})"
    

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

# @admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('Studnt_Name', 'Seat_no', 'booking_time', 'timming', 'duration')
    list_filter = ('status',)
    search_fields = ('getStuName', 'seat')
    form = CustomBookingForm

    actions = ['custom_bulk_delete']

    def timming(self,modelObject):
        return f"{self.convertToReadableTimeing(f"{modelObject.start_time}")} to {self.convertToReadableTimeing(f"{modelObject.end_time}")}"
    
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
        js = ('admin/js/jquery.init.js',  # Make sure jQuery is loaded before your custom script
              'booking/js/booking_admin.js',)  # Your custom JavaScript file
    def Studnt_Name(self,modelObject):
        return modelObject.student.name

    def Seat_no(self,modelObject):
        return modelObject.seat.seat_id
    
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
        if not change:
            obj.created_by = request.user
        obj.save()

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
    list_display = ('seat_id','location','start_and_end_timing', 'status')
    # list_filter = ('status',)
    list_filter = ('location','status')  # Filter by location
    search_fields = ('seat_id','status','location__description')  # Allows search by seat ID and location description

    # def showLocationName(self,modelObject):
    #     return f'{modelObject.location.location_name} '

    def start_and_end_timing(self, modelObject):
        # Filter bookings for the specific seat
        seatObj = Booking.objects.filter(seat=modelObject)

        # Aggregate to get the earliest start_time and the latest end_time
        start_time = seatObj.aggregate(start_time=Min('start_time'))['start_time']
        end_time = seatObj.aggregate(end_time=Max('end_time'))['end_time']

        # # Check if both times exist
        if start_time and end_time:
            # Return the duration between start and end times
            # duration = end_time - start_time
            return f'{start_time} - {end_time}'
        else:
            return 'no booking'
        # return '333'

    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created
            obj.created_by = request.user
        obj.save()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'location':
            # Filter locations based on the current user
            formfield.queryset = Location.objects.filter(created_by=request.user)
        return formfield

# @admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_no', 'adhar_no', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'phone_no', 'adhar_no')

    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created
            obj.created_by = request.user
        obj.save()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'location':
            # Filter locations based on the current user
            formfield.queryset = Location.objects.filter(created_by=request.user)
        return formfield

# Re-register UserAdmin
# admin_site.unregister(User)

# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')  # Example fields
class Monthly_prizingAdmin(admin.ModelAdmin):
    list_display = ('hours', 'prize', 'discription', 'status')
    list_filter = ('status','hours', 'prize')
    search_fields = ('hours', 'phone_no')
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('booking_to_update', 'prize', 'payment_time')
    list_filter = ('payment_time', 'prize')
    search_fields = ('prize',)

admin_site.register(Payments,PaymentsAdmin)
admin_site.register(Monthly_prizing,Monthly_prizingAdmin)
admin_site.register(Seat,SeatAdmin)
admin_site.register(Location,LocationAdmin)
admin_site.register(Booking,BookingAdmin)
admin_site.register(Student,StudentAdmin)

