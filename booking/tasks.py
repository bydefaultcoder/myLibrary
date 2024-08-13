from celery import shared_task # type: ignore
from .models import Booking

@shared_task
def update_booking_status():
    bookings = Booking.objects.filter(status='active')
    for booking in bookings:
        booking.check_and_update_status()
