from django.shortcuts import render, redirect, get_object_or_404
from .models import Process1,ProcessInterval1
from .forms import ProcessForm, ProcessIntervalFormSet
from datetime import datetime, timedelta
from itertools import groupby
from django.utils import timezone

def process_list1(request):
    processes = Process1.objects.prefetch_related('intervals').all().order_by('created_at')
    
    grouped_processes = []
    
    # Group by main_process and sub_process
    for key, group in groupby(processes, key=lambda p: (p.main_process, p.sub_process)):
        grouped_processes.append(list(group))

    # Get current time
    now = datetime.now()
    start_time = now - timedelta(hours=0)  # Start from 1 hour before current time
    end_time = now + timedelta(hours=6)    # End at 5 hours after current time

    time_intervals = []
    start_time = start_time.replace(second=0, microsecond=0, minute=(start_time.minute // 10) * 10)  # Round down to the nearest 10 minutes

    while start_time < end_time:
        next_time = start_time + timedelta(minutes=10)
        time_range = f"{start_time.strftime('%I:%M %p')}-{next_time.strftime('%I:%M %p')}"
        time_intervals.append(time_range)
        start_time = next_time

    for group in grouped_processes:
        for process in group:
            start_infos = []
            end_infos = []
            startend_infos = []
            
            # Get the additional_info directly from the process
            additional_info = process.additional_info  

            for interval in process.intervals.all():
                if interval.start_time:
                    formatted_start_time = interval.start_time.strftime('%I:%M %p')
                    next_start_time = (datetime.combine(datetime.today(), interval.start_time) + timedelta(minutes=10)).strftime('%I:%M %p')
                    time_range = f"{formatted_start_time}-{next_start_time}"
                    start_infos.append({'time_range': time_range, 'info': interval.start_info})

                if interval.end_time:
                    formatted_end_time = interval.end_time.strftime('%I:%M %p')
                    next_end_time = (datetime.combine(datetime.today(), interval.end_time) + timedelta(minutes=10)).strftime('%I:%M %p')
                    time_range = f"{formatted_end_time}-{next_end_time}"
                    end_infos.append({'time_range': time_range, 'info': interval.end_info})

                if interval.startend_time:
                    formatted_startend_time = interval.startend_time.strftime('%I:%M %p')
                    next_startend_time = (datetime.combine(datetime.today(), interval.startend_time) + timedelta(minutes=10)).strftime('%I:%M %p')
                    time_range = f"{formatted_startend_time}-{next_startend_time}"
                    startend_infos.append({'time_range': time_range, 'info': interval.start_info})

            # Attach start, end, and startend information to the process
            process.start_infos = start_infos
            process.end_infos = end_infos
            process.startend_infos = startend_infos
            process.additional_info = additional_info  # Store additional info

    return render(request, 'process_list1.html', {
        'grouped_processes': grouped_processes,
        'time_intervals': time_intervals,
    })

def process_full(request):
    processes = Process1.objects.prefetch_related('intervals').all().order_by('created_at')
    
    grouped_processes = []
    
    # Group by main_process and sub_process
    for key, group in groupby(processes, key=lambda p: (p.main_process, p.sub_process)):
        grouped_processes.append(list(group))

    time_intervals = []
    start_time = datetime.strptime('08:30', '%H:%M')
    end_time = datetime.strptime('00:00', '%H:%M') + timedelta(days=1)

    while start_time < end_time:
        next_time = start_time + timedelta(minutes=10)
        time_intervals.append(f"{start_time.strftime('%I:%M %p')}-{next_time.strftime('%I:%M %p')}")
        start_time = next_time

    for group in grouped_processes:
        for process in group:
            start_infos = []
            end_infos = []
            startend_infos = []
            
            # Get the additional_info directly from the process
            additional_info = process.additional_info  

            for interval in process.intervals.all():
                if interval.start_time:
                    formatted_start_time = interval.start_time.strftime('%I:%M %p')
                    next_start_time = (datetime.combine(datetime.today(), interval.start_time) + timedelta(minutes=10)).strftime('%I:%M %p')
                    time_range = f"{formatted_start_time}-{next_start_time}"
                    start_infos.append({'time_range': time_range, 'info': interval.start_info})

                if interval.end_time:
                    formatted_end_time = interval.end_time.strftime('%I:%M %p')
                    next_end_time = (datetime.combine(datetime.today(), interval.end_time) + timedelta(minutes=10)).strftime('%I:%M %p')
                    time_range = f"{formatted_end_time}-{next_end_time}"
                    end_infos.append({'time_range': time_range, 'info': interval.end_info})

                if interval.startend_time:
                    formatted_startend_time = interval.startend_time.strftime('%I:%M %p')
                    next_startend_time = (datetime.combine(datetime.today(), interval.startend_time) + timedelta(minutes=10)).strftime('%I:%M %p')
                    time_range = f"{formatted_startend_time}-{next_startend_time}"
                    startend_infos.append({'time_range': time_range, 'info': interval.start_info})


            # Attach start, end, and startend information to the process
            process.start_infos = start_infos
            process.end_infos = end_infos
            process.startend_infos = startend_infos
            process.additional_info = additional_info  # Store additional info

    return render(request, 'process_list1.html', {
        'grouped_processes': grouped_processes,
        'time_intervals': time_intervals,
    })

def process_add1(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():  # Ensure the form is valid
            form.save()  # Save the Process instance
            return redirect('process_list1')  # Redirect to the process list after saving
    else:
        form = ProcessForm()  # Initialize an empty form on GET request

    return render(request, 'process_add1.html', {'form': form})

def process_edit1(request, pk):
    process = get_object_or_404(Process1, pk=pk)
    
    if request.method == 'POST':
        form = ProcessForm(request.POST, instance=process)
        formset = ProcessIntervalFormSet(request.POST, instance=process)
        
        if form.is_valid() and formset.is_valid():
            form.save()  # Save the main process
            intervals = formset.save(commit=False)  # Do not commit yet
            
            for interval in intervals:
                interval.process = process  # Associate the interval with the process
                
                # No calculation for startend_time, leave it as is (if it's filled, it's saved; if not, it stays empty)
                interval.save()  # Now save the interval

            return redirect('process_list1')
    else:
        form = ProcessForm(instance=process)
        formset = ProcessIntervalFormSet(instance=process)  # Fetch existing intervals

    return render(request, 'process_edit1.html', {
        'form': form,
        'formset': formset,
    })

def process_edit2(request,pk):
    process = get_object_or_404(Process1, pk=pk)
    if request.method == 'POST':
        formset = ProcessIntervalFormSet(request.POST, instance=process)

        if formset.is_valid():
            intervals = formset.save(commit=False)  # Do not commit yet

            for interval in intervals:
                interval.process = process  # Associate the interval with the process

                # Ensure that start_time and end_time are valid
                if interval.start_time and interval.end_time:
                    start_dt = datetime.combine(timezone.now().date(), interval.start_time)
                    end_dt = datetime.combine(timezone.now().date(), interval.end_time)

                    # Check if end_time is later than start_time
                    if end_dt <= start_dt:
                        formset.errors.append("End time must be later than start time.")
                        return render(request, 'process_edit2.html', {'formset': formset})

                    # Calculate midpoint for startend_time
                    interval.startend_time = (start_dt + (end_dt - start_dt) / 2).time()

                interval.save()  # Now save the interval

            return redirect('process_list1')  # Redirect to the process list after saving

    else:
        formset = ProcessIntervalFormSet(queryset=ProcessInterval1.objects.none())  # Ensures empty formset on GET

    return render(request, 'process_edit2.html', {'formset': formset})

