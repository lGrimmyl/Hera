# Generated by Django 4.2.6 on 2023-12-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident_reports', '0009_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentreport',
            name='is_emergency',
            field=models.BooleanField(default=False),
        ),
    ]