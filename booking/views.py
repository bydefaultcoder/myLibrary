from  datetime import time
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MonthlyPlan, Seat, Booking,Location
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
# @login_required
def get_seats_by_location(request):
    location_id = request.GET.get('location_id')
    location = Location.objects.get(location_id=location_id)
    seats = location.seats.exclude(status='removed')
    print(seats,"here")
    seat_dict = {seat.pk: f"seatNo:{seat.seat_no}" for seat in seats}
    return JsonResponse(seat_dict)

@login_required
def get_seat_available_timing(request):
    """
    API view to get available hours for a specific seat based on already booked slots.
    """
    seat_id = request.GET.get('seat_id')
    joining_date = request.GET.get('joining_date')
    seat = Seat.objects.get(seat_id=seat_id)
    
    return JsonResponse(seat.filter_available_hours(joining_date))

@login_required
def get_mothlyplans_by_user(request):
    """
    API view to get available hours for a specific seat based on already booked slots.
    """
    currentUserPK = request.GET.get('currentUserPK')
    print(currentUserPK)
    plans = MonthlyPlan.objects.filter(created_by =currentUserPK)
    print(plans)
    
    return JsonResponse({"data":list(plans.values())})
    
