from django.contrib.admin import SimpleListFilter
# import datetime

from .models import Location


# class PublishedThisYearFilter(SimpleListFilter):
class SeatFilterByLocations(SimpleListFilter):
    title = 'Library'  # Filter title
    parameter_name = 'library'  # URL query parameter name

    def lookups(self, request, model_admin):
        # Define the options for filtering
        locations = Location.objects.filter(created_by=request.user)
        list_of_locations = [(i.pk,i.location_name) for i in locations]
        return list_of_locations

    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(location=self.value())
        return queryset
