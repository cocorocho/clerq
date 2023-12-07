from typing import Any

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from tinymce.widgets import TinyMCE

from core.widgets import AppointmentTimeWidget, FlatpickrDateWidget
from appointments.models import Appointment


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        disable_fields = kwargs.pop("disable_fields", False)
        super().__init__(*args, **kwargs)

        if disable_fields:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = Appointment
        fields = (
            "client_name",
            "subject",
            "details",
            "appointed_staff",
            "appointment_date",
            "appointment_time",
        )
        widgets = {
            "details": TinyMCE(),
            "appointment_date": FlatpickrDateWidget(
                attrs={
                    # Time picker will communicate through ref
                    "x-ref": "appointmentDatePicker",
                    "hidden": True,
                },
                flatpickr_attrs={"inline": True, "disable_previous_dates": True},
            ),
            "appointment_time": AppointmentTimeWidget(format="%H:%M"),
        }


class AppointmentConclusionForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("conclusion_details",)
        widgets = {"conclusion_details": TinyMCE()}

    def save(self, commit: bool = True) -> Any:
        self.instance.conclude_appointment()

        return super().save(commit)


class AppointmentFilterForm(forms.Form):
    appointment_date = forms.CharField(
        required=False,
        widget=FlatpickrDateWidget(flatpickr_attrs={"mode": "range"}),
        initial=now().date(),
    )
    # appointment_date_end = forms.CharField(required=False, widget=FlatpickrDateWidget())
    appointed_staff = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.filter(role="APTE"),
        widget=forms.SelectMultiple(attrs={"class": "!h-full"}),
        required=False,
    )
