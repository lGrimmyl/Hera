# Generated by Django 4.2.6 on 2024-01-19 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_is_police_station'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='User_ID',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
