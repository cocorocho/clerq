from collections import defaultdict

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from tinymce.models import HTMLField

from accounts.models import User
from core.base.models import BaseModel
from appointments.utils import get_appointment_periods


def get_deleted_user() -> User:
    """Get or Create user named 'deleted_user'"""
    return get_user_model().objects.get_or_create(username="deleted_user")[0]


class Appointment(BaseModel):
    subject = models.CharField(
        max_length=200,
        verbose_name=_("appointment subject"),
    )
    details = HTMLField(
        verbose_name=_("appointment details"),
        blank=True,
    )
    client_name = models.CharField(max_length=100, verbose_name=_("client name"))
    appointed_staff = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET(get_deleted_user),
        verbose_name=_("appointed staff"),
        related_name="appointments",
    )
    appointer_staff = models.ForeignKey(
        # To be populated automatically by current user
        to=get_user_model(),
        on_delete=models.SET(get_deleted_user),
        editable=False,
        related_name="created_appointments",
        verbose_name="appointer staff",
    )
    appointment_date = models.DateField(verbose_name=_("appointment date"))
    appointment_time = models.TimeField(verbose_name=_("appointment time"))
    is_concluded = models.BooleanField(
        default=False,
        editable=False,
        verbose_name=_("appointment concluded"),
    )
    is_canceled = models.BooleanField(
        default=False, editable=False, verbose_name=_("appointment canceled")
    )
    # Timestamp for appointment is concluded
    conclusion_date = models.DateTimeField(editable=False, blank=True, null=True)
    conclusion_details = HTMLField(blank=True, verbose_name=_("conclusion details"))

    class Meta:
        verbose_name = _("appointment")
        verbose_name_plural = _("appointments")
        ordering = ("appointment_date", "appointment_time")
        constraints = (
            models.UniqueConstraint(
                fields=["appointment_date", "appointment_time"],
                name="appointment_unique_by_datetime",
            ),
        )

    @classmethod
    def get_unavailable_datetimes(cls) -> dict:
        """
        Group all booked hours under date as dict

        Example:
            {
                '2022-02-22': ['14:30', '15:30', '19:20']
            }
        """
        queryset = (
            cls.objects.filter(appointment_date__gte=now())
            .values("appointment_date", "appointment_time")
            .order_by("appointment_date", "appointment_time")
        )
        result = defaultdict(list)
        for i in queryset:
            result[str(i["appointment_date"])].append(
                i["appointment_time"].strftime("%H:%M")
            )

        return dict(result)
