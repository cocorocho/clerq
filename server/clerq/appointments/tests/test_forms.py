from django import forms
from django.test import TestCase

from model_bakery import baker

from appointments.models import Appointment
from appointments.forms import AppointmentForm


class AppointmentFormTestCase(TestCase):
    def setUp(self) -> None:
        self.form_class = AppointmentForm

    def test_create_appointment(self) -> None:
        appointer_staff = baker.make("accounts.User")
        staff = baker.make("accounts.User")
        appointment = baker.prepare(Appointment)

        form_data = {
            "client_name": appointment.client_name,
            "subject": appointment.subject,
            "details": appointment.subject,
            "appointed_staff": staff,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
        }

        form = self.form_class(data=form_data)

        form.is_valid()
        form.instance.appointer_staff = appointer_staff
        form.save()

        self.assertTrue(Appointment.objects.filter(**form_data).exists())

    def test_appointment_datetime_errors(self) -> None:
        appointer_staff = baker.make("accounts.User")
        staff = baker.make("accounts.User")

        # Create an appointment
        appointment = baker.make(Appointment)
        # Dummy appointment
        new_appointment = baker.prepare(Appointment)

        form_data = {
            "client_name": new_appointment.client_name,
            "subject": new_appointment.subject,
            "details": new_appointment.subject,
            "appointed_staff": staff,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
        }

        form = self.form_class(data=form_data)
        self.assertFalse(form.is_valid())
