from django.contrib.auth.models import AbstractUser
from django.db import models
from incident_reports.models import IncidentReport
import datetime
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os


class ValidIDType(models.Model):
    id_type = models.CharField(max_length=100)

    def __str__(self):
        return self.id_type


class CustomUser(AbstractUser):
    is_police_station = models.BooleanField(default=False)
    Valid_ID = models.ImageField(upload_to='photos/', null=True, blank=True)
    valid_id_type = models.ForeignKey(
        ValidIDType, on_delete=models.SET_NULL, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    citizenship = models.CharField(max_length=255, null=True, blank=True)
    civil_status = models.CharField(max_length=255, null=True, blank=True)
    placeofbirth = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    highesteducationattainment = models.CharField(
        max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'Citizen'

        constraints = []
        indexes = []
        unique_together = []

        permissions = [
            ('can_have_photo', 'Can have a photo'),
        ]


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'accounts':
        # Add test users here if needed
        # They will automatically be created after migrating the db
        users = [
            # Superadmin Account
            # Username is required here for creating the superuser
            {
                'email': os.getenv('DJANGO_ADMIN_EMAIL'),
                'username': os.getenv('DJANGO_ADMIN_USERNAME'),
                'password': os.getenv('DJANGO_ADMIN_PASSWORD'),
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Hera',
                'last_name': 'Admin'
            },
        ]

        for user in users:
            if not CustomUser.objects.filter(email=user['email']).exists():
                if (user['is_superuser']):
                    USER = CustomUser.objects.create_superuser(
                        username=user['username'],
                        email=user['email'],
                        password=user['password'],
                    )
                    print('Created Superuser:', user['email'])
                else:
                    USER = CustomUser.objects.create_user(
                        username=user['username'],
                        email=user['email'],
                        password=user['password'],
                    )
                    print('Created User:', user['email'])

                USER.first_name = user['first_name']
                USER.last_name = user['last_name']
                USER.is_active = True
                USER.save()
