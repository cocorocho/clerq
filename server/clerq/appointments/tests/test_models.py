from datetime import datetime, timezone

from django.test import TestCase
from django.db import IntegrityError

from model_bakery import baker


from appointments.models import Appointment


class AppointmentTestCase(TestCase):
    def test_get_unavailable_appointment_datetimes(self) -> None:
        dates = [
            datetime(2099, 2, 2, 15, 30, tzinfo=timezone.utc),
            datetime(2099, 2, 2, 14, 30, tzinfo=timezone.utc),
            datetime(2099, 3, 3, 10, 50, tzinfo=timezone.utc),
            datetime(2085, 4, 4, 8, 40, tzinfo=timezone.utc),
        ]

        [
            baker.make(
                Appointment, appointment_date=date.date(), appointment_time=date.time()
            )
            for date in dates
        ]
        result = Appointment.get_unavailable_datetimes()
        target = {
            "2085-04-04": ["08:40"],
            "2099-02-02": ["14:30", "15:30"],
            "2099-03-03": ["10:50"],
        }
        self.assertEqual(result, target)

    def test_appointment_datetime_unique_validation_raises_validationerror(
        self,
    ) -> None:
        appointment = baker.make(Appointment, is_concluded=False)

        with self.assertRaises(IntegrityError):
            baker.make(
                Appointment,
                appointment_date=appointment.appointment_date,
                appointment_time=appointment.appointment_time,
                is_concluded=False,
            )
