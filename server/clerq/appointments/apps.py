from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "appointments"

    """
    Time format is `H:M`
    Example:
        "8:00"
        "8:30"
        "14:25"
        "23:5"
    """
    working_hours = ("8:00", "16:00")
    appointment_period = 30  # minutes
