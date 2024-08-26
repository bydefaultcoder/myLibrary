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

def get_seats_by_location(request):
    location_id = request.GET.get('location_id')
    print(Location.objects.filter(location_id=location_id)[0])
    seats = Seat.objects.filter(location_id=location_id, created_by = request.user)
    seat_dict = {seat.pk: f"seatNo:{seat.seat_no}" for seat in seats}
    return JsonResponse(seat_dict)

def get_seat_available_timing(request):
    """
    API view to get available hours for a specific seat based on already booked slots.
    """
    seat_id = request.GET.get('seat_id')
    joining_date = request.GET.get('joining_date')
    seat = Seat.objects.get(seat_id=seat_id)
    
    return JsonResponse(_filter_available_hours(seat,joining_date))

def _filter_available_hours(seat,joining_date):
    """
    Filter the start and end time options based on already booked slots for the seat.
    """
    # Get existing bookings for this seat
    booked_slots = Booking.objects.filter(seat=seat)

    # Get all full hours from 00:00 to 23:00
    all_hours = [time(hour=h) for h in range(24)]  # Generates times like 00:00:00, 01:00:00, ..., 23:00:00

    # Initialize the list for storing unavailable hours
    unavailable_hours = set()

    # Mark unavailable hours based on existing bookings
    for booking in booked_slots:
        booked_slots.payments
        if booked_slots.payments :
            start_hour = booking.start_time.hour
            end_hour = booking.end_time.hour

            # Mark all hours between the start and end times as unavailable
            unavailable_hours.update(range(start_hour+1, end_hour))  # Include all hours between start and end

    # Filter out unavailable hours to get the available ones
    print(all_hours)
    print(unavailable_hours)
    available_hours = [hour for hour in all_hours if hour.hour not in unavailable_hours]

    available_choices = [hour.hour for hour in available_hours]

    print(available_choices)

    return {"data":available_choices}

# def _filter_available_hours(seat):
#     """
#     Filter the start and end time options based on already booked slots for the seat.
#     """
#     # Get existing bookings for this seat
#     booked_slots = Booking.objects.filter(seat=seat)

#     # Get all full hours from 00:00 to 23:00
#     all_hours = [time(hour=h) for h in range(24)]  # Generates times like 00:00:00, 01:00:00, ..., 23:00:00

#     # Initialize the list for storing unavailable hours
#     unavailable_hours = set()

#     # Mark unavailable hours based on existing bookings
#     for booking in booked_slots:
#         start_hour = booking.start_time.hour
#         end_hour = booking.end_time.hour

#         # Mark all hours between the start and end times as unavailable
#         unavailable_hours.update(range(start_hour+1, end_hour))  # Include all hours between start and end

#     # Filter out unavailable hours to get the available ones
#     print(all_hours)
#     print(unavailable_hours)
#     available_hours = [hour for hour in all_hours if hour.hour not in unavailable_hours]

#     available_choices = [hour.hour for hour in available_hours]

#     print(available_choices)

#     return {"data":available_choices}

def get_mothlyplans_by_user(request):
    """
    API view to get available hours for a specific seat based on already booked slots.
    """
    currentUserPK = request.GET.get('currentUserPK')
    print(currentUserPK)
    plans = MonthlyPlan.objects.filter(created_by =currentUserPK)
    print(plans)
    
    return JsonResponse({"data":list(plans.values())})
    
