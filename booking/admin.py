from django.contrib import admin
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
from django.db.models import Min, Max
import logging
from django.utils.html import format_html
from django.utils import timezone as tz
from dateutil.relativedelta import relativedelta
logger = logging.getLogger(__name__)


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
            return '--'
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
            # Filter locations based on the current user
            formfield.queryset = Location.objects.filter(created_by=request.user)
        if db_field.name == 'student':
            # Filter locations based on the current user
            formfield.queryset = Student.objects.filter(created_by=request.user)
        return formfield



# -----------------------------------------------------
# for student
from django import forms
class ImagePreviewWidget(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        # Get the basic output from the super class
        output = super().render(name, value, attrs, renderer)
        
        # Image preview HTML if there's an existing image
        preview_html = ''
        if value and hasattr(value, 'url'):
            preview_html = format_html(
                '<img id="image-preview" src="{}" style="max-width: 200px; max-height: 200px; margin-bottom: 10px;"/><br/>', 
                value.url
            )
        
        # JavaScript to update the image preview
        js_script = format_html('''
            <script type="text/javascript">
                document.getElementById('{input_id}').onchange = function(event) {{
                    var reader = new FileReader();
                    reader.onload = function(e) {{
                        var img = document.getElementById('image-preview');
                        if (!img) {{
                            img = document.createElement('img');
                            img.id = 'image-preview';
                            img.style.maxWidth = '200px';
                            img.style.maxHeight = '200px';
                            img.style.marginBottom = '10px';
                            var inputElement = document.getElementById('{input_id}');
                            inputElement.parentNode.insertBefore(img, inputElement);
                        }}
                        img.src = e.target.result;
                    }};
                    reader.readAsDataURL(event.target.files[0]);
                }};
            </script>
        ''', input_id=attrs['id'])

        # Combine preview HTML, the output of the original widget, and the JS script
        return format_html('{}{}{}', preview_html, output, js_script)
# @admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('stu_no','name', 'phone_no', 'adhar_no','image_tag', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'phone_no', 'adhar_no')

    class Meta:
        ordering = ['stu_no']  # Sorts by title in ascending order

    def get_queryset(self, request):
        # Only show objects created by the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    def image_tag(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.avatar.url))

    image_tag.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created
            obj.created_by = request.user
        obj.save()
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'location':
            formfield.queryset = Location.objects.filter(created_by=request.user)
        return formfield
    
    def days_to_expire(self,modelObject):
        booking  = Booking.objects.filter(student = modelObject.pk).latest("pk")
        if  booking != None:
            objects  = Payment.objects.filter(booking=booking.pk)
            print(object.query)
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
        else:
            "Seat not alloted"
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'avatar':
            kwargs['widget'] = ImagePreviewWidget()
        return super().formfield_for_dbfield(db_field, **kwargs)

# Re-register UserAdmin
# admin_site.unregister(User)

# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')  # Example fields
class MonthlyPlanAdmin(admin.ModelAdmin):
    list_display = ('hours', 'prize', 'discription', 'status')
    list_filter = ('status','hours', 'prize')
    search_fields = ('hours', 'phone_no')

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
admin_site.register(Student,StudentAdmin)
# from admin_interface.models import Theme
# from django.contrib import admin

# admin_site.register(Theme)
