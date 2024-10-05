from django import forms
from .models import Process1, ProcessInterval1
from django.forms import inlineformset_factory
from datetime import timedelta, datetime

class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process1
        fields = ['main_process', 'sub_process','additional_info']

class ProcessIntervalForm(forms.ModelForm):
    class Meta:
        model = ProcessInterval1
        fields = ['start_time', 'end_time', 'startend_time', 'start_info', 'end_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial values if editing
        if self.instance.pk:
            # Check if start_time, end_time, and startend_time are not None
            if self.instance.start_time:
                start_dt = datetime.combine(datetime.today(), self.instance.start_time)
                self.fields['start_time'].initial = f"{start_dt:%H:%M}-{(start_dt + timedelta(minutes=10)):%H:%M}"
            if self.instance.end_time:
                end_dt = datetime.combine(datetime.today(), self.instance.end_time)
                self.fields['end_time'].initial = f"{end_dt:%H:%M}-{(end_dt + timedelta(minutes=10)):%H:%M}"
            if self.instance.startend_time:
                startend_dt = datetime.combine(datetime.today(), self.instance.startend_time)
                self.fields['startend_time'].initial = f"{startend_dt:%H:%M}-{(startend_dt + timedelta(minutes=10)):%H:%M}"

        # Set fields to be optional
        self.fields['start_time'].required = False
        self.fields['end_time'].required = False
        self.fields['startend_time'].required = False
        self.fields['start_info'].required = False
        self.fields['end_info'].required = False
    
# Create a formset to handle the ProcessInterval objects using the custom form
ProcessIntervalFormSet = inlineformset_factory(
    Process1,
    ProcessInterval1,
    form=ProcessIntervalForm,
    fields=['start_time', 'end_time', 'startend_time', 'start_info', 'end_info'],
    extra=1,  
)
