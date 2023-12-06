from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        """Role Enum"""

        APPOINTER = ("APTR", _("Appointing User"))  # Receptionist, Clerk ...
        APPOINTEE = ("APTE", _("Appointee User"))  # Doctor, Lawyer, Advisor ...

    role = models.CharField(
        max_length=4, choices=RoleChoices.choices, default=RoleChoices.APPOINTER
    )
