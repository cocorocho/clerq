import json
from datetime import timedelta, date
from typing import Any

from django.forms import Widget, TimeInput
from django.utils.timezone import now
from django.forms.renderers import BaseRenderer
from django.utils.safestring import SafeText

from appointments.models import Appointment
from appointments.utils import get_appointment_periods


class AppointmentTimeWidget(TimeInput):
    template_name = "forms/widgets/timeselector.html"

    def __init__(self, attrs: dict | None = None, format: str | None = None) -> None:
        if attrs is None:
            attrs = {}

        attrs["hidden"] = True
        super().__init__(attrs, format)

    def get_context(self, name: str, value: Any, attrs: dict | None) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        context["booked_times"] = Appointment.get_unavailable_datetimes()
        context["times"] = get_appointment_periods()
        return context


class FlatpickrDateWidget(Widget):
    """Date widget using flatpickr js"""

    template_name = "forms/widgets/flatpickr_date.html"

    def __init__(
        self, attrs: dict | None = None, flatpickr_attrs: dict | None = None
    ) -> None:
        if attrs is None:
            attrs = {}
        if not flatpickr_attrs:
            flatpickr_attrs = {}

        # Make input hidden
        attrs["hidden"] = True

        self.flatpickr_attrs = flatpickr_attrs
        super().__init__(attrs)

    def get_context(self, name: str, value: Any, attrs: dict = {}) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)

        # Default AlpineJs attrs to inject calendar
        self.add_flatpickr_attrs_to_context(context)

        return context

    def add_flatpickr_attrs_to_context(self, context: dict) -> str:
        """
        Add flatpickr attributes to widget context
        """
        input_value = context["widget"]["value"]
        disable_previous_dates = self.flatpickr_attrs.pop(
            "disable_previous_dates", False
        )

        # If input has initial value, set it as default via flatpickr config
        if input_value:
            self.flatpickr_attrs.update({"defaultDate": input_value})
        if disable_previous_dates:
            disable_date_start = (
                # If input date is before today's date, start from the day before input date
                (date.fromisoformat(input_value) - timedelta(days=1)).strftime(
                    "%Y-%m-%d"
                )
                if (input_value and (date.fromisoformat(input_value) < now().date()))
                else "1900-01-01"
            )
            self.flatpickr_attrs.update(
                {
                    "disable": [
                        {
                            "from": "1900-01-01",
                            "to": disable_date_start
                            or (now() - timedelta(days=1)).date().strftime("%Y-%m-%d"),
                        }
                    ]
                }
            )

        context["widget"]["attrs"].update(
            {
                "x-init": f"flatpickr({context['widget']['attrs']['id']}, {json.dumps(self.flatpickr_attrs)})"
            }
        )
