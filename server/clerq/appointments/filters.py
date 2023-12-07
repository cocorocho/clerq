from django.contrib.auth import get_user_model
from django.utils.formats import date_format

from django_filters import FilterSet, filters

from appointments.models import Appointment, AppointmentQuerySet


class AppointmentFilterSet(FilterSet):
    appointment_date = filters.CharFilter(method="filter_appointment_date")
    appointed_staff = filters.ModelMultipleChoiceFilter(
        queryset=get_user_model().objects.filter(role="APTE")
    )

    class Meta:
        model = Appointment
        fields = ("appointment_date",)

    def filter_appointment_date(
        self, queryset: AppointmentQuerySet, name: str, value: str
    ) -> AppointmentQuerySet:
        """Filter `appoitnment_date` by range or exact date"""

        filter_expression = ""

        if value and "to" in value:
            value = [i.strip() for i in value.split("to")]
            filter_expression = "__range"

        return queryset.filter(**{f"{name}{filter_expression}": value})

    @property
    def qs(self):
        return self.queryset.filter(appointment_date="2023-12-07")
        return super().qs
