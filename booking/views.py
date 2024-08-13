from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Seat, Booking,Location
from django.contrib import messages


# @login_required
def index(request):
    seats = Seat.objects.all()
    return render(request, 'booking/index.html', {'seats': seats})


# @login_required
def book_seat(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)

    if seat.status == 'Available':
        # Create a new booking
        booking = Booking.objects.create(
            user=request.user,
            seat=seat,
            status='Active'
        )
        # Update seat status
        seat.status = 'Booked'
        seat.save()
        messages.success(request, 'Seat booked successfully!')
    else:
        messages.error(request, 'Seat is already booked.')

    return redirect('index')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status == 'Active':
        # Update booking status
        booking.status = 'Canceled'
        booking.save()
        # Update seat status
        seat = booking.seat
        seat.status = 'Available'
        seat.save()
        messages.success(request, 'Booking canceled successfully!')
    else:
        messages.error(request, 'Booking is already canceled or invalid.')

    return redirect('index')

def get_seats_by_location(request):
    location_id = request.GET.get('location_id')
    print(Location.objects.filter(location_id=location_id)[0])
    seats = Seat.objects.filter(location_id=location_id)
    seat_dict = {seat.pk: str(seat) for seat in seats}
    return JsonResponse(seat_dict)
