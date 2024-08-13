from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:seat_id>/', views.book_seat, name='book_seat'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]