from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    page_size = 3  # Items per page
    page_size_query_param = 'page_size'  # Allow the client to set page size (optional)
    max_page_size = 3  # Maximum allowed page size (optional)
