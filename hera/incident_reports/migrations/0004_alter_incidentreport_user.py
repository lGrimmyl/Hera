# Generated by Django 4.2.6 on 2023-12-05 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incident_reports', '0003_incidentreport_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentreport',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='incident_reports', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]