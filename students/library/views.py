from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view

from booking.models import Location
from students.library.pagination import MyPagination

from .dbQueries import get_libraries

from .LibratySerializers import LocationSerializer
from django.http import JsonResponse


@api_view(['get'])
def all_libraries(request):
    # Fetch data using raw SQL
    paginator = MyPagination()  # Use your custom pagination class    # Calculate limit and offset for the SQL query
    paginator.paginate_queryset(queryset=[],request=request)
    print(paginator.page.start_index(),paginator.page_size)
    offset = paginator.page.start_index()  # Start index is 1-based, but SQL `LIMIT` is 0-based
    if not offset==0:
        offset = offset -1
    limit = paginator.page_size

    # Modify the SQL query to add pagination (LIMIT and OFFSET)
    paginated_query = f" LIMIT {limit} OFFSET {offset}"


    data = get_libraries(paginated_query)
    # data = Location.objects.filter(status="exposed")
    
    serializer = LocationSerializer(data, many=True)
    print(paginator.get_next_link())
    response_data = {
        'count': len(data),
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': serializer.data
    }
    print(response_data)
    # return paginator.get_paginated_response(serializer.data)
    return Response(response_data)


