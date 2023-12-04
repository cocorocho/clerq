from datetime import datetime, timezone

from django.test import TestCase
from django.apps import apps

from model_bakery import baker

from appointments.utils import get_appointment_periods


class AppointmentUtilsTestCase(TestCase):
    def test_get_appointment_periods(self) -> None:
        app = apps.get_app_config("appointments")

        app.working_hours = ("8:00", "10:30")
        app.appointment_period = 30

        target = [
            ["08:00", "08:30"],
            ["08:30", "09:00"],
            ["09:00", "09:30"],
            ["09:30", "10:00"],
            ["10:00", "10:30"],
        ]

        self.assertEqual(get_appointment_periods(), target)

        # Test odd times
        app.working_hours = ("8:55", "10:23")
        app.appointment_period = 13

        target = [
            ["08:55", "09:08"],
            ["09:08", "09:21"],
            ["09:21", "09:34"],
            ["09:34", "09:47"],
            ["09:47", "10:00"],
            ["10:00", "10:13"],
            ["10:13", "10:26"],
        ]

        self.assertEqual(get_appointment_periods(), target)
