from django.shortcuts import render, redirect, get_object_or_404
from .models import Process,ProcessInterval
from .forms import ProcessForm, ProcessIntervalFormSet
from datetime import datetime, timedelta
from itertools import groupby
from django.utils import timezone
from status.models import Process1,ProcessInterval1
from .forms import SignUpForm,LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def button_page(request):
    if request.method == 'POST':
        if 'admin' in request.POST:
            return redirect('login')
        elif 'user' in request.POST:
            return redirect('loginu')
    return render(request, 'button_page.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('admin')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user')  # Redirect to your desired page
            else:
                # Return an 'invalid login' error message.
                return render(request, 'loginu.html', {'form': form, 'error_message': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'loginu.html', {'form': form})

VALID_USERNAME = 'admin'
VALID_PASSWORD = 'res@123'

def login1_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                # Redirect to the main page or a protected page
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def process_list(request):
    processes = Process.objects.prefetch_related('intervals').all().order_by('created_at')
    
    grouped_processes = []
    
    # Group by main_process and sub_process
    for key, group in groupby(processes, key=lambda p: (p.main_process, p.sub_process)):
        grouped_processes.append(list(group))

    time_intervals = []
    start_time = datetime.strptime('08:30', '%H:%M')
    end_time = datetime.strptime('00:00', '%H:%M') + timedelta(days=1)

    while start_time < end_time:
        next_time = start_time + timedelta(minutes=10)
        time_intervals.append(f"{start_time.strftime('%H:%M')}-{next_time.strftime('%H:%M')}")
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
                    formatted_start_time = interval.start_time.strftime('%H:%M')
                    next_start_time = (datetime.combine(datetime.today(), interval.start_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_start_time}-{next_start_time}"
                    start_infos.append({'time_range': time_range, 'info': interval.start_info})

                if interval.end_time:
                    formatted_end_time = interval.end_time.strftime('%H:%M')
                    next_end_time = (datetime.combine(datetime.today(), interval.end_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_end_time}-{next_end_time}"
                    end_infos.append({'time_range': time_range, 'info': interval.end_info})

                if interval.startend_time:
                    formatted_startend_time = interval.startend_time.strftime('%H:%M')
                    next_startend_time = (datetime.combine(datetime.today(), interval.startend_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_startend_time}-{next_startend_time}"
                    startend_infos.append({'time_range': time_range, 'info': interval.start_info})

            # Attach start, end, and startend information to the process
            process.start_infos = start_infos
            process.end_infos = end_infos
            process.startend_infos = startend_infos
            process.additional_info = additional_info  # Store additional info

    return render(request, 'process_list.html', {
        'grouped_processes': grouped_processes,
        'time_intervals': time_intervals,
    })

def process_add(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        formset = ProcessIntervalFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            process = form.save()  # Save the Process instance
            intervals = formset.save(commit=False)  # Do not commit yet

            for interval in intervals:
                interval.process = process  # Associate the interval with the process

                # Ensure that start_time and end_time are valid
                if interval.start_time and interval.end_time and interval.startend_time:
                    start_dt = datetime.combine(timezone.now().date(), interval.start_time)
                    end_dt = datetime.combine(timezone.now().date(), interval.end_time)
                    startend_dt = datetime.combine(timezone.now().date(), interval.startend_time)

                    # Check if end_time is later than start_time
                    if end_dt <= start_dt:
                        formset.errors.append("End time must be later than start time.")
                        return render(request, 'process_add.html', {'form': form, 'formset': formset})

                interval.save()  # Now save the interval

            return redirect('process_list')  # Redirect to the process list after saving

    else:
        form = ProcessForm()
        formset = ProcessIntervalFormSet(queryset=ProcessInterval.objects.none())  # Ensures empty formset on GET

    return render(request, 'process_add.html', {'form': form, 'formset': formset})

def process_edit(request, pk):
    process = get_object_or_404(Process, pk=pk)
    
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

            return redirect('process_list')
    else:
        form = ProcessForm(instance=process)
        formset = ProcessIntervalFormSet(instance=process)  # Fetch existing intervals

    return render(request, 'process_edit.html', {
        'form': form,
        'formset': formset,
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import ProcessInterval1
from .forms import ProcessForm1, ProcessIntervalFormSet1
from datetime import datetime, timedelta
from itertools import groupby
from django.utils import timezone
import pandas as pd

def Home(request):
    return render(request, 'Home.html')

def process_list1(request):
    processes = Process.objects.prefetch_related('intervals1').all().order_by('created_at')
    
    grouped_processes = []
    
    # Group by main_process and sub_process
    for key, group in groupby(processes, key=lambda p: (p.main_process, p.sub_process)):
        grouped_processes.append(list(group))

    # Get current time
    now = datetime.now()
    start_time = now.replace(second=0, microsecond=0, minute=(now.minute // 10) * 10)  # Round down to the nearest 10 minutes
    end_time = now + timedelta(hours=6)    # End at 6 hours after current time

    time_intervals = []

    while start_time < end_time:
        next_time = start_time + timedelta(minutes=10)
        time_range = f"{start_time.strftime('%H:%M')}-{next_time.strftime('%H:%M')}"
        time_intervals.append(time_range)
        start_time = next_time

    for group in grouped_processes:
        for process in group:
            start_infos = []
            end_infos = []
            startend_infos = []
            
            additional_info = process.additional_info  

            for interval in process.intervals1.all():  # Use intervals1 only
                if interval.start_time:
                    formatted_start_time = interval.start_time.strftime('%H:%M')
                    next_start_time = (datetime.combine(datetime.today(), interval.start_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_start_time}-{next_start_time}"
                    start_infos.append({'time_range': time_range, 'info': interval.start_info})

                if interval.end_time:
                    formatted_end_time = interval.end_time.strftime('%H:%M')
                    next_end_time = (datetime.combine(datetime.today(), interval.end_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_end_time}-{next_end_time}"
                    end_infos.append({'time_range': time_range, 'info': interval.end_info})

                # Use the correct attribute name here
                if interval.startend_time:  
                    formatted_startend_time = interval.startend_time.strftime('%H:%M')
                    next_startend_time = (datetime.combine(datetime.today(), interval.startend_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_startend_time}-{next_startend_time}"
                    startend_infos.append({'time_range': time_range, 'info': interval.start_info})  # Change 'start_info' if necessary

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
    processes = Process.objects.prefetch_related('intervals1').all().order_by('created_at')
    
    grouped_processes = []
    
    # Group by main_process and sub_process
    for key, group in groupby(processes, key=lambda p: (p.main_process, p.sub_process)):
        grouped_processes.append(list(group))

    time_intervals = []
    start_time = datetime.strptime('08:30', '%H:%M')
    end_time = datetime.strptime('00:00', '%H:%M') + timedelta(days=1)

    while start_time < end_time:
        next_time = start_time + timedelta(minutes=10)
        time_intervals.append(f"{start_time.strftime('%H:%M')}-{next_time.strftime('%H:%M')}")
        start_time = next_time

    for group in grouped_processes:
        for process in group:
            start_infos = []
            end_infos = []
            startend_infos = []            
            additional_info = process.additional_info  

            for interval in process.intervals1.all():  # Use intervals1 only
                if interval.start_time:
                    formatted_start_time = interval.start_time.strftime('%H:%M')
                    next_start_time = (datetime.combine(datetime.today(), interval.start_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_start_time}-{next_start_time}"
                    start_infos.append({'time_range': time_range, 'info': interval.start_info})

                if interval.end_time:
                    formatted_end_time = interval.end_time.strftime('%H:%M')
                    next_end_time = (datetime.combine(datetime.today(), interval.end_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_end_time}-{next_end_time}"
                    end_infos.append({'time_range': time_range, 'info': interval.end_info})

                if interval.startend_time:
                    formatted_startend_time = interval.startend_time.strftime('%H:%M')
                    next_startend_time = (datetime.combine(datetime.today(), interval.startend_time) + timedelta(minutes=10)).strftime('%H:%M')
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
        form = ProcessForm1(request.POST)
        if form.is_valid():  # Ensure the form is valid
            form.save()  # Save the Process instance
            return redirect('process_list1')  # Redirect to the process list after saving
    else:
        form = ProcessForm1()  # Initialize an empty form on GET request

    return render(request, 'process_add1.html', {'form': form})


def process_edit2(request,pk):
    process = get_object_or_404(Process, pk=pk)
    if request.method == 'POST':
        formset = ProcessIntervalFormSet1(request.POST, instance=process)

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
        formset = ProcessIntervalFormSet1(queryset=ProcessInterval1.objects.none())  # Ensures empty formset on GET

    return render(request, 'process_edit2.html', {'formset': formset})





