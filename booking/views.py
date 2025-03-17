from  datetime import time
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from booking.forms.Library_form import LibraryForm
from booking.forms.Seat_from import SeatForm
from booking.forms.plan_form import MonthlyPlanForm
from booking.forms.seat_allotement_form import BookingForm

from .models import MonthlyPlan, Seat, Booking,Location
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest,HttpResponseRedirect
from django.db.models import Min, Max ,Count, Q
# @login_required
def index(request):
    seats = Seat.objects.all()
    return render(request, 'booking/index.html', {'seats': seats})


@login_required
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
@csrf_exempt  # Disable CSRF for API-like views (only if necessary)
def get_seats(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        try:
            # Try parsing JSON data first
            if request.content_type == 'application/json':
                data = json.loads(request.body)  # Parse JSON body
            else:
                data = request.POST  # Use form-encoded data
            
            print("Received data:", data)

            type_map = {
                "d": 1,
                "m": 30,
                "w": 7,
            }

            location_id = data.get('location_id')
            if not location_id:
                return JsonResponse({'status': 'error', 'message': 'Location ID is required'}, status=400)

            joining_date = data.get('joining_date')
            plan = data.get('plan').split("_")
            hour = int(plan[0])
            planing_for = plan[2]
            duration = int(plan[3])
            multiple = int(data.get('multiple', 1))  # Default to 1 if not provided

            location = Location.objects.get(location_id=location_id)
            seats = location.seats.exclude(status='removed')
            seat_dict = {}

            for seat in seats:
                timming_data = seat.filter_available(joining_date, hour, duration * multiple * type_map[planing_for])
                seat_dict[seat.pk] = [f"seatNo:{seat.seat_no}", timming_data["timming"]]

            return JsonResponse(seat_dict)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
def start_and_end_timing(modelObject):
    # Filter bookings for the specific seat
    if modelObject.status == 'removed':
        return "Removed"
    seatObj = Booking.objects.filter(seat=modelObject)
    # Aggregate to get the earliest start_time and the latest end_time
    start_time = seatObj.aggregate(start_time=Min('start_time'))['start_time']
    end_time = seatObj.aggregate(end_time=Max('end_time'))['end_time']

    if start_time and end_time:
        return f'{start_time.strftime("%I%p")} to {end_time.strftime("%I%p")}'
    else:
        return 'Not alloted (Active)'

@login_required
def get_seat_available_timing(request:HttpRequest):
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

# lib-----------------------------start
@login_required    
def get_lib(request):
    libraries = Location.objects.all().filter(created_by=request.user)
    print(libraries)
    return render(request,'customadmin/library.html',{"data":libraries})

@login_required    
def create_lib(request):
    if request.method == "POST":
        form = LibraryForm(request.POST)
        if form.is_valid():
            print(hasattr(request, 'user'),"---------has attri")
            qr = form.save(commit=False)
            qr.created_by = request.user  # Set the creator
            qr.save()
            return redirect('seat')  # Redirect to a success page
    else:
        form = LibraryForm()
    
    return render(request, "customadmin/library_form.html", {"form": form})

@login_required    
def add_seat(request):
    if request.method == "POST":
        form = SeatForm(request.POST)
        if form.is_valid():
            qr = form.save(commit=False)
            qr.created_by = request.user  # Set the creator
            qr.save()
            return redirect('lib')  # Redirect to a success page
    else:
        form = SeatForm()
    
    return render(request, "customadmin/seat_form.html", {"form": form})
# lib-----------------------------end

@login_required
def get_seat(request):
    seat = Seat.objects.all().filter(created_by=request.user).order_by('seat_no')
    # print(libraries)
    return render(request,'customadmin/seats.html',{"data":seat})
@login_required
def get_plan(request):
    plan = MonthlyPlan.objects.all()
    # print(libraries)
    return render(request,'customadmin/plans.html',{"data":plan})

# from django.shortcuts import render, redirect
# from .forms import MonthlyPlanForm
@login_required
def create_plan(request):
    if request.method == "POST":
        form = MonthlyPlanForm(request.POST)
        if form.is_valid():
            qr = form.save(commit=False)
            qr.created_by = request.user  # Set the creator
            qr.save()
            return redirect('plan')  # Redirect to the list page
    else:
        form = MonthlyPlanForm()

    return render(request, "customadmin/plan_form.html", {"form": form})
@login_required
def get_booking(request):
    alllotment = Booking.objects.all().filter(created_by=request.user)
    # print(libraries)
    return render(request,'customadmin/seat_allotement.html',{"data":alllotment})

@login_required
def seat_allotment(request):
    if request.method == "POST":
        form = BookingForm(request.POST, request=request)
        if form.is_valid():
            qr = form.save(commit=False)
            qr.created_by = request.user  # Set the creator
            qr.save()
            return redirect('booking')  # Redirect to the list page
    else:
        form = BookingForm(None, request=request)
    return render(request, "customadmin/seat_allotement_form.html", {"form": form})
