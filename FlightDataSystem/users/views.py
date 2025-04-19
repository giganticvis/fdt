import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .forms import FlightForm, CcdForm, OepForm
from .models import Flight, Log

def home(request):
    return render(request, 'users/home.html')

@login_required
def foi_fod_dashboard(request):
    if request.user.role != 'foi_fod':
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

    if request.method == 'POST':
        flight_id = request.POST.get('flight_id')
        if flight_id:  # Editing an existing flight
            flight = get_object_or_404(Flight, id=flight_id)
            if not flight.is_editable():
                messages.error(request, 'This flight can no longer be edited.')
                return redirect('foi_fod_dashboard')
            form = FlightForm(request.POST, instance=flight)
        else:  # Creating a new flight
            form = FlightForm(request.POST)

        if form.is_valid():
            flight = form.save(commit=False)
            flight.created_by = request.user
            flight.save()
            Log.objects.create(user=request.user, action='edit', details=f"Edited flight {flight.flight_number}")
            messages.success(request, 'Flight data saved successfully.')
            return redirect('foi_fod_dashboard')
    else:
        form = FlightForm()

    flights = Flight.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'users/foi_fod_dashboard.html', {'form': form, 'flights': flights})

@login_required
def ccd_dashboard(request):
    if request.user.role != 'ccd':
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

    if request.method == 'POST':
        flight_id = request.POST.get('flight_id')
        flight = get_object_or_404(Flight, id=flight_id)
        if not flight.is_editable():
            messages.error(request, 'This flight can no longer be edited.')
            return redirect('ccd_dashboard')
        form = CcdForm(request.POST, instance=flight)
        if form.is_valid():
            flight = form.save(commit=False)
            flight.save()
            Log.objects.create(user=request.user, action='edit', details=f"Edited flight {flight.flight_number}")
            messages.success(request, 'Cabin crew data saved successfully.')
            return redirect('ccd_dashboard')
    else:
        form = CcdForm()

    return render(request, 'users/ccd_dashboard.html', {'form': form})

@login_required
def oep_dashboard(request):
    if request.user.role != 'oep':
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

    if request.method == 'POST':
        flight_id = request.POST.get('flight_id')
        flight = get_object_or_404(Flight, id=flight_id)
        if not flight.is_editable():
            messages.error(request, 'This flight can no longer be edited.')
            return redirect('oep_dashboard')
        form = OepForm(request.POST, instance=flight)
        if form.is_valid():
            flight = form.save(commit=False)
            flight.save()
            Log.objects.create(user=request.user, action='edit', details=f"Edited flight {flight.flight_number}")
            messages.success(request, 'OEP data saved successfully.')
            return redirect('oep_dashboard')
    else:
        form = OepForm()

    return render(request, 'users/oep_dashboard.html', {'form': form})

@login_required
def super_admin_dashboard(request):
    if request.user.role != 'super_admin':
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

    flights = Flight.objects.all()
    return render(request, 'users/super_admin_dashboard.html', {'flights': flights})

@login_required
def export_flight_data(request):
    if request.user.role != 'super_admin':
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="flight_data.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow([
        'Date', 'Flight Number', 'Aircraft Registration', 'Flight Crew', 'SN Crew', 'Cabin Crew',
        'AFL Number', 'From', 'To', 'Air Time (Hrs)', 'Air Time (Mins)', 'Block Time (Hrs)',
        'Block Time (Mins)', 'Fuel Uplift (Liters)', 'Sp. Gravity', 'Temp (°C)', 'Fuel Added (kg)',
        'Total Fuel (tons)', 'Fuel Burnt (tons)', 'Remaining Fuel (tons)', 'Mail (kg)', 'Cargo (kg)',
        'Pax', 'Weight (kg)'
    ])

    # Write data rows
    flights = Flight.objects.all()
    for flight in flights:
        writer.writerow([
            flight.date, flight.flight_number, flight.aircraft_registration, flight.flight_crew,
            flight.sn_crew, flight.cabin_crew, flight.afl_number, flight.from_location,
            flight.to_location, flight.air_time_hrs, flight.air_time_mins, flight.block_time_hrs,
            flight.block_time_mins, flight.fuel_uplift_liters, flight.sp_gravity, flight.temp_c,
            flight.fuel_added_kg, flight.total_fuel_tons, flight.fuel_burnt_tons,
            flight.remaining_fuel_tons, flight.mail_kg, flight.cargo_kg, flight.pax, flight.weight_kg
        ])

    return response

def get_flights(request):
    date = request.GET.get('date')
    flights = Flight.objects.filter(date=date).values('id', 'flight_number')
    return JsonResponse({'flights': list(flights)})

@login_required
def view_logs(request):
    if request.user.role != 'super_admin':
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

    logs = Log.objects.all().order_by('-timestamp')
    return render(request, 'users/view_logs.html', {'logs': logs})
