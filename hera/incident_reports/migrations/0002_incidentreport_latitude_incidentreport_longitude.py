# Generated by Django 4.2.6 on 2023-11-14 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident_reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentreport',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='incidentreport',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
