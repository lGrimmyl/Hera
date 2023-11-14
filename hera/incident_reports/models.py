from django.db import models
from django.urls import reverse

# Create your models here.

class IncidentReport(models.Model):  
    photo = models.ImageField(upload_to='incident_photos/', blank=True, null=True)
    description = models.TextField()
    datetime_reported = models.DateTimeField(auto_now_add=True)
    narrative = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"Incident Report on {self.datetime_reported.strftime('%Y-%m-%d %H:%M')}"
    
    def get_absolute_url(self):
        return reverse('report-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-datetime_reported']

    