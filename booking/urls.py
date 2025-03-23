from django.urls import path
from . import vender_views

urlpatterns = [
    path('', vender_views.index, name='index'),
    path('book/<int:seat_id>/', vender_views.book_seat, name='book_seat'),
    path('cancel/<int:booking_id>/', vender_views.cancel_booking, name='cancel_booking'),
]