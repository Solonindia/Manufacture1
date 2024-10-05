from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import DailyProduction
import json
from django.utils import timezone
from datetime import datetime, timedelta
import pytz

def production_dashboard(request):
    today = timezone.now().date()  # Get current date in the timezone
    india_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(india_tz)

    # Restrict access between 12 AM and 8:30 AM
    if now.hour == 0 or (now.hour < 8 or (now.hour == 8 and now.minute < 30)):
        return HttpResponse("Error: The program cannot be run between 12:00 AM and 8:30 AM.")

    # Round current time to the next 10-minute interval
    current_time = now.replace(second=0, microsecond=0)
    if current_time.minute % 10 != 0:
        current_time += timedelta(minutes=(10 - current_time.minute % 10))

    # Define time bounds for production intervals
    start_bound = current_time.replace(hour=8, minute=30, second=0, microsecond=0)
    end_bound = current_time.replace(hour=23, minute=59, second=0, microsecond=0)

    # Create lists for past, current, and future time intervals
    past_times = []
    current_times = []
    future_times = []

    # Generate past times (8:30 AM to current time)
    temp_time = start_bound
    while temp_time < current_time:
        end_interval = temp_time + timedelta(minutes=10)
        past_times.append(f"{temp_time.strftime('%H:%M')} - {end_interval.strftime('%H:%M')}")
        temp_time += timedelta(minutes=10)

    # Current times (current time to current time + 6 hours)
    temp_time = current_time
    end_current = current_time + timedelta(hours=6)
    while temp_time <= end_current:
        end_interval = temp_time + timedelta(minutes=10)
        current_times.append(f"{temp_time.strftime('%H:%M')} - {end_interval.strftime('%H:%M')}")
        temp_time += timedelta(minutes=10)

    # Future times (after current time + 6 hours to midnight)
    start_future = current_time + timedelta(hours=6)
    temp_time = start_future
    while temp_time <= end_bound:
        end_interval = temp_time + timedelta(minutes=10)
        future_times.append(f"{temp_time.strftime('%H:%M')} - {end_interval.strftime('%H:%M')}")
        temp_time += timedelta(minutes=10)

    # Fetch today's production record or create a new one
    production_record, created = DailyProduction.objects.get_or_create(
        date=today,
        defaults={
            'pellet_manufacturing': 'Pellet Manufacturing',
            'battery_assembly': 'Battery Assembly',
            'project_name': 'Project',
            'operator': 'Operator',
            'pellet_manufacturing1': 'Pellet Manufacturing',
            'drying_of_pellets': 'Drying of pellets',
            'moisture_content_test': 'Moisture Content test',
            'storage': 'Storage',
            'mixing_of_anode_powder': 'Mixing of Anode Powder',
            'pellet_manufacturing_anode': 'Pellet Manufacturing Anode',
            'transfer_of_electrodes_and_components': 'Transfer of electrodes and components',
            'cell_assembly': 'Cell Assembly',
            'stack_assembly': 'Stack Assembly',
            'stack_insulation_wrapping': 'Stack insulation wrapping',
            'spot_welding_of_terminals': 'Spot welding of terminals',
            'stack_drying': 'Stack Drying',
            'battery_welding': 'Battery welding',
            'leak_check_for_batteries': 'Leak check for batteries',
            'static_parameters_inspection': 'Static parameters inspection',
            'handover_to_qc': 'Handover to QC',
            'operator1': 'Anuradha, Pranay',
            'operator2': 'A. Srinivas, Laxman',
            'operator3': 'Naidu, Ramu',
            'operator4': 'Pranay',
            'operator5': 'Laxman',
            'operator6': 'Ramu',
            'operator7': 'Ramu',
            'operator8': 'Naidu',
            'operator9': 'Naidu, Ramu',
            'operator10': 'Laxmi Kumari',
            'operator11': 'Krishnaji',
            'operator12': 'Anji',
            'operator1p': 'Electrolyte',
            'operator2p': 'Cathode',
            'operator3p': 'Heat pellet',
            'operator4p': 'Electrolyte',
            'operator5p': 'Cathode',
            'operator6p': 'Heat pellet',
            'operator7p': 'Electrolyte',
            'operator8p': 'Cathode'
        }
    )

    # Send the production record and time intervals to the template
    return render(request, 'dashboard.html', {
        'production_values': [production_record],  # Display today's record
        'past_times': past_times,
        'current_times': current_times,
        'future_times': future_times,
        'is_new_record': created,  # To show if the record was newly created
    })

def save_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            production_id = data.get('id')
            field_name = data.get('field')
            new_value = data.get('value')

            # Fetch the production record and update the field
            production_record = get_object_or_404(DailyProduction, id=production_id)
            setattr(production_record, field_name, new_value)
            production_record.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'failed'}, status=400)
