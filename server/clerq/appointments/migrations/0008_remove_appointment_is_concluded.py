# Generated by Django 4.2.7 on 2023-12-04 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0007_appointment_is_concluded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='is_concluded',
        ),
    ]
