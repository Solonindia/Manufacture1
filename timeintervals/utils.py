from datetime import timedelta
from django.utils import timezone
from .models import Process, Process1

def combine_datetime(date, time):
    """Helper function to combine date and time into a datetime object."""
    return timezone.datetime.combine(date, time)

def compare_process_times():
    standard_processes = Process.objects.prefetch_related('intervals').all()
    daily_processes = Process1.objects.prefetch_related('intervals').all()
    
    comparison_results = {}

    for standard_process in standard_processes:
        standard_intervals = standard_process.intervals.all()
        daily_processes_matching = daily_processes.filter(
            main_process=standard_process.main_process,
            sub_process=standard_process.sub_process
        )

        for daily_process in daily_processes_matching:
            daily_intervals = daily_process.intervals.all()

            for standard_interval in standard_intervals:
                unique_key = (
                    standard_process.main_process or '',
                    standard_process.sub_process or '',
                    standard_interval.start_time,
                    standard_interval.end_time,
                    standard_interval.startend_time,
                )

                if unique_key not in comparison_results:
                    comparison_results[unique_key] = {
                        'main_process': standard_process.main_process or '',
                        'sub_process': standard_process.sub_process or '',
                        'standard_start_time': standard_interval.start_time,  # Store time object
                        'actual_start_time': None,  # Store as None initially
                        'standard_end_time': standard_interval.end_time,  # Store time object
                        'actual_end_time': None,
                        'standard_startend_time': standard_interval.startend_time,  # Store time object
                        'actual_startend_time': None,
                        'start_delay': timedelta(0),
                        'end_delay': timedelta(0),
                        'difference': '',
                        'status': '',
                        'planned_time': 0,
                        'actual_time': 0,
                    }

                for daily_interval in daily_intervals:
                    today = timezone.now().date()
                    
                    # Compare start time
                    if daily_interval.start_time and standard_interval.start_time:
                        actual_start_datetime = combine_datetime(today, daily_interval.start_time)
                        standard_start_datetime = combine_datetime(today, standard_interval.start_time)

                        if comparison_results[unique_key]['actual_start_time'] is None:
                            comparison_results[unique_key]['actual_start_time'] = daily_interval.start_time  # Keep as time object

                        if actual_start_datetime > standard_start_datetime:
                            comparison_results[unique_key]['start_delay'] = actual_start_datetime - standard_start_datetime

                    # Compare end time
                    if daily_interval.end_time and standard_interval.end_time:
                        actual_end_datetime = combine_datetime(today, daily_interval.end_time)
                        standard_end_datetime = combine_datetime(today, standard_interval.end_time)

                        if comparison_results[unique_key]['actual_end_time'] is None:
                            comparison_results[unique_key]['actual_end_time'] = daily_interval.end_time  # Keep as time object
                        
                        if actual_end_datetime > standard_end_datetime:
                            comparison_results[unique_key]['end_delay'] = actual_end_datetime - standard_end_datetime

                    # Compare startend time
                    if daily_interval.startend_time and standard_interval.startend_time:
                        actual_startend_datetime = combine_datetime(today, daily_interval.startend_time)
                        standard_startend_datetime = combine_datetime(today, standard_interval.startend_time)

                        if comparison_results[unique_key]['actual_startend_time'] is None:
                            comparison_results[unique_key]['actual_startend_time'] = daily_interval.startend_time  # Keep as time object
                        
                        if actual_startend_datetime > standard_startend_datetime:
                            comparison_results[unique_key]['startend_delay'] = actual_startend_datetime - standard_startend_datetime

                if (comparison_results[unique_key]['actual_start_time'] and 
                    comparison_results[unique_key]['actual_end_time']):
                    
                    standard_start_datetime = combine_datetime(today, standard_interval.start_time)
                    standard_end_datetime = combine_datetime(today, standard_interval.end_time)
                    actual_start_datetime = combine_datetime(today, comparison_results[unique_key]['actual_start_time'])
                    actual_end_datetime = combine_datetime(today, comparison_results[unique_key]['actual_end_time'])

                    standard_duration = (standard_end_datetime - standard_start_datetime).total_seconds() / 60
                    actual_duration = (actual_end_datetime - actual_start_datetime).total_seconds() / 60

                    comparison_results[unique_key]['planned_time'] = standard_duration
                    comparison_results[unique_key]['actual_time'] = actual_duration

                    difference = actual_duration - standard_duration
                    comparison_results[unique_key]['difference'] = abs(difference)

                    if difference < 0:
                        comparison_results[unique_key]['status'] = 'Fast'
                    elif difference > 0:
                        comparison_results[unique_key]['status'] = 'Delay'
                    else:
                        comparison_results[unique_key]['status'] = 'On Time'

    return list(comparison_results.values())
