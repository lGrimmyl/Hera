# Generated by Django 4.2.6 on 2023-12-10 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_police_station',
            field=models.BooleanField(default=False),
        ),
    ]
