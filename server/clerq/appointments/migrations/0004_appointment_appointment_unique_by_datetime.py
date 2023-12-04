# Generated by Django 4.2.7 on 2023-11-29 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_alter_appointment_options_appointment_is_canceled'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(fields=('appointment_date', 'appointment_time'), name='appointment_unique_by_datetime'),
        ),
    ]
