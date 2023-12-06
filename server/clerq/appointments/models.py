from collections import defaultdict

from django.db import models
from django.db.models import OuterRef, Exists
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from tinymce.models import HTMLField

from core.base.models import BaseModel, BaseManager, BaseQuerySet
from accounts.models import User


def get_deleted_user() -> User:
    """Get or Create user named 'deleted_user'"""
    return get_user_model().objects.get_or_create(username="deleted_user")[0]


class AppointmentQuerySet(BaseQuerySet):
    """Appointment QuerySet"""

    def scheduled(self) -> models.QuerySet:
        return self.filter(conclusion_date__isnull=True)

    def concluded_appointments(self) -> models.QuerySet:
        return self.filter(conclusion_date__isnull=False)

    def filter_today(self) -> models.QuerySet:
        return self.filter(appointment_date=now().date()).order_by("-appointment_time")

    def get_current_appointment_for_user(self, user: User) -> models.QuerySet:
        """Get currently active appointment for user"""

        return self.filter(in_progress=True, appointed_staff=user).first()

    def with_appointee_is_busy(self) -> models.QuerySet:
        """Annotate whethever `appointed_staff` has an `Appointment` in progress"""

        return self.annotate(
            appointee_is_busy=Exists(
                Appointment.objects.filter(
                    appointed_staff=OuterRef("appointed_staff"), in_progress=True
                )
            )
        )


class Appointment(BaseModel):
    objects = BaseManager.from_queryset(AppointmentQuerySet)()

    # Creation Fields
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
    is_canceled = models.BooleanField(
        default=False, editable=False, verbose_name=_("appointment canceled")
    )
    in_progress = models.BooleanField(
        default=False, editable=False, verbose_name=_("appointment in progress")
    )

    # Conclusion Fields
    # Timestamp for appointment is concluded
    conclusion_date = models.DateTimeField(editable=False, blank=True, null=True)
    conclusion_details = HTMLField(blank=True, verbose_name=_("conclusion details"))

    class Meta:
        verbose_name = _("appointment")
        verbose_name_plural = _("appointments")
        ordering = ("appointment_date", "-appointment_time")
        constraints = (
            models.UniqueConstraint(
                fields=["appointment_date", "appointment_time"],
                name="appointment_unique_by_datetime",
            ),
            models.UniqueConstraint(
                fields=["appointed_staff"],
                condition=models.Q(in_progress=True),
                name="single_active_appointment_per_appointed_staff",
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

    def conclude_appointment(self, commit: bool = False) -> None:
        """
        Conclude `Appointment`, add timestamp to `conclusion_date` and set `in_progress` to `False`
        """
        if self.conclusion_details:
            self.conclusion_date = now()
            self.in_progress = False

            if commit:
                self.save()

    def takein_appointment(self, commit: bool = False) -> None:
        """Take in an appointment"""

        self.in_progress = True

        if commit:
            self.save()
