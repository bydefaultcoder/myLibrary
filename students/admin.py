from django.contrib import admin

from customAdmin.admin import admin_site 
# from myLibrary.customAdmin.customAdminForm import CustomUserCreationForm
from booking.models import Payment, Student,Booking,Location
# from django.db import transaction
# from django.contrib import messages
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
# from django.contrib.auth.models import Group
# from django.db.models import Min, Max ,Count, Q
import logging
from django.utils.html import format_html
from django.utils import timezone as tz
from dateutil.relativedelta import relativedelta
import csv
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
import json

from .studentCreationForm import StudentCreationForm
logger = logging.getLogger(__name__)
# Register your models here.
from django import forms

class StudentAdmin(admin.ModelAdmin):
    add_form = StudentCreationForm
    # update_form
    list_display = ('getName','phone_no','image_tag', 'address')
    def getName(self,modelObj):
        return f'{modelObj.first_name} {modelObj.last_name}'
    getName.short_description = "Full Name"

    # list_filter = ('status',)
    search_fields = ('first_name','last_name', 'phone_no', 'adhar_no')
    actions = ['export_as_csv']


    fieldsets = (   
        (None, {'fields': ( 'phone_no','first_name','last_name','avatar')}),
        ('More Info', {'fields': ('email','adhar_no','address')}),
        # ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','phone_no','first_name','last_name', 'avatar'),
        }),
    )


    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
           row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    
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

admin_site.register(Student,StudentAdmin)