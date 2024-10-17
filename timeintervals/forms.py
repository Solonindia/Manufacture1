from django import forms
from .models import Process, ProcessInterval
from django.forms import inlineformset_factory,BaseInlineFormSet
from datetime import timedelta, datetime

class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['main_process', 'sub_process','add_info']

class ProcessIntervalForm(forms.ModelForm):
    class Meta:
        model = ProcessInterval
        fields = ['start_time', 'end_time', 'startend_time', 'start_info', 'end_info']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Generate time choices for dropdown
        self.fields['start_time'].choices = self.generate_time_choices()
        self.fields['end_time'].choices = self.generate_time_choices()
        self.fields['startend_time'].choices = self.generate_time_choices()

        # Set initial values if editing
        if self.instance.pk:
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

    def generate_time_choices(self):
        choices = []
        start_time = 8 * 60 + 30  # 08:30 AM in minutes
        end_time = 24 * 60  # Midnight in minutes

        while start_time < end_time:
            start_hour = start_time // 60
            start_minute = start_time % 60
            end_time_slot = start_time + 10  # Next 10-minute slot
            end_hour = end_time_slot // 60
            end_minute = end_time_slot % 60

            time_value = f"{start_hour:02}:{start_minute:02}-{end_hour:02}:{end_minute:02}"
            choices.append((time_value, time_value))  # Add as both value and label
            start_time += 10  # Increment by 10 minutes

        return choices

# Custom formset without delete checkbox
class ProcessIntervalFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the delete checkbox from each form
        for form in self.forms:
            form.fields.pop('DELETE', None)

# Create the inline formset using the custom formset class
ProcessIntervalFormSet = inlineformset_factory(
    Process,
    ProcessInterval,
    form=ProcessIntervalForm,
    formset=ProcessIntervalFormSet,
    fields=['start_time', 'end_time', 'startend_time', 'start_info', 'end_info'],
    extra=0,  
)

from django import forms
from .models import ProcessInterval1
from django.forms import inlineformset_factory
from datetime import timedelta, datetime

class ProcessForm1(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['main_process', 'sub_process','add_info']

class ProcessIntervalForm1(forms.ModelForm):
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
ProcessIntervalFormSet1 = inlineformset_factory(
    Process,
    ProcessInterval1,
    form=ProcessIntervalForm1,
    fields=['start_time', 'end_time', 'startend_time', 'start_info', 'end_info'],
    extra=1,  
)


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

