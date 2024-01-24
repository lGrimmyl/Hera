# Generated by Django 5.0.1 on 2024-01-24 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident_reports', '0014_incidentreport_closed_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidentreport',
            name='photo',
        ),
        migrations.AddField(
            model_name='incidentreport',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='incident_media/'),
        ),
        migrations.AddField(
            model_name='incidentreport',
            name='media_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]