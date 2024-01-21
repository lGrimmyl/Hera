from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class IncidentCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class IncidentSubcategory(models.Model):
    category = models.ForeignKey(IncidentCategory, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name





class IncidentReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=False, 
        related_name='incident_reports')
    is_user_victim = models.BooleanField(default=False)
    is_emergency = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='incident_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    datetime_reported = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    narrative = models.TextField( blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    subcategories = models.ManyToManyField(IncidentSubcategory, blank=True)
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    CLOSED = 'Closed'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In Progress'),
        (CLOSED, 'Closed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=OPEN,
    )
    def save(self, *args, **kwargs):
        if self.status == 'Closed' and self.closed_at is None:
            self.closed_at = timezone.now()
        super(IncidentReport, self).save(*args, **kwargs)

    def __str__(self):
        return f"Incident Report on {self.datetime_reported.strftime('%Y-%m-%d %H:%M')}"
    
    def get_absolute_url(self):
        return reverse('report-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-datetime_reported']

class Suspect(models.Model):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='suspects')
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    affix_name = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    birthdate = models.CharField(max_length=255)
    gender = models.CharField(max_length=6)
    contact_number = models.CharField(max_length=255)
    citizenship = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    waddress = models.CharField(max_length=255)


class Victim(models.Model):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='victims')
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, null = True)
    civil_status = models.CharField(max_length=255)
    birthdate = models.CharField(max_length=255)
    gender = models.CharField(max_length=6)
    contact_number = models.CharField(max_length=255)
    citizenship = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    highesteducationattainment = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255, null = True)

class ChildConflict(models.Model):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='child_conflicts')
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=11)
    email = models.CharField(max_length=255, null = True)
    homecontact_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.recipient.username}'