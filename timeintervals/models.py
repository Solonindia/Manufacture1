from django.db import models

class Process(models.Model):
    main_process = models.CharField(max_length=100, null=True)
    sub_process = models.CharField(max_length=100, null=True)
    additional_info = models.CharField(max_length=255, blank=True)  # New additional info field
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.main_process

class ProcessInterval(models.Model):
    process = models.ForeignKey(Process, related_name='intervals', on_delete=models.CASCADE)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    startend_time = models.TimeField(null=True)
    start_info = models.CharField(max_length=100, blank=True)
    end_info = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

from django.db import models


class ProcessInterval1(models.Model):
    process = models.ForeignKey(Process, related_name='intervals1', on_delete=models.CASCADE)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    startend_time = models.TimeField(null=True)
    start_info = models.CharField(max_length=100, blank=True)
    end_info = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

