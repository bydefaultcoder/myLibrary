from django.contrib import admin
from .BookingForm import CustomBookingForm
from .models import Student,Seat,Booking,Location
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


@admin.register(Location)
class location(admin.ModelAdmin):
    # list_display
    list_display = ('display_name','number_of_seats','discription',)
    def display_name(self,modelObject):
        return f"{modelObject.location_name}-({modelObject.location_id})"
    

    def save_model(self, request, obj, form, change):
        print(change,obj)
        if not change:  # If the object is being created
            obj.created_by = request.user
        obj.save()
    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('Studnt_Name', 'Seat_no', 'booking_time', 'status', 'duration')
    list_filter = ('status',)
    search_fields = ('getStuName', 'seat')
    form = CustomBookingForm

    actions = ['custom_bulk_delete']

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
                print(queryset)
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
    
    def get_form_kwargs(self, request, obj=None):
        # Ensure we pass the request to the form
        kwargs = super().get_form_kwargs(request, obj)
        kwargs['request'] = request
        print(kwargs['request'])
        return kwargs
    
    def save_model(self, request, obj, form, change):
        print(change,obj)
        if not change:
            obj.created_by = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        # print(db_field,"here")
        if db_field.name == 'student':
            formfield.queryset = Student.objects.filter(created_by=request.user)
        if db_field.name == 'seat' :
            # Filter locations based on the current user
            formfield.queryset = Seat.objects.filter(created_by=request.user)
        return formfield


    # def save_model(self, request, obj, form, change):
    #     # Here, request.user is the currently logged-in admin
    #     print(request,obj)
    #     if not change:  # If creating a new object
    #         obj.created_by = request.user
    #     obj.save()

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    # actions = ['custom_delete']
    list_display = ('seat_id','location', 'status')
    # list_filter = ('status',)
    list_filter = ('location','status')  # Filter by location
    search_fields = ('seat_id','status','location__description')  # Allows search by seat ID and location description

    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        print(change,obj)
        if not change:  # If the object is being created
            obj.created_by = request.user
        obj.save()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'location':
            # Filter locations based on the current user
            formfield.queryset = Location.objects.filter(created_by=request.user)
        return formfield



@admin.register(Student)
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
        print(change,obj)
        if not change:  # If the object is being created
            obj.created_by = request.user
        obj.save()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'location':
            # Filter locations based on the current user
            formfield.queryset = Location.objects.filter(created_by=request.user)
        return formfield