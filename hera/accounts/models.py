from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    Valid_ID = models.ImageField(upload_to='photos/', null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    citizenship = models.CharField(max_length=255, null=True, blank=True)
    civil_status = models.CharField(max_length=255, null=True, blank=True)
    placeofbirth = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    highesteducationattainment = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'Citizen'
        # Add these lines to resolve the reverse accessor conflicts
        constraints = []
        indexes = []
        unique_together = []

        # These related_name changes will resolve the conflicts
        permissions = [
            ('can_have_photo', 'Can have a photo'),
        ]