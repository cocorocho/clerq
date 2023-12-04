from datetime import datetime, timedelta

from django.apps import apps


def get_appointment_periods() -> list[tuple[str, str]]:
    """
    Get available appointment times by periods.
    Period is defined by `appointment_period` in app config

    Example:
        [
            ("15:00", "15:30"),
            ("15:30", "16:00"),
            ("16:00", "16:30"),
            ...
        ]
    """

    app = apps.get_app_config("appointments")
    time_format = "%H:%M"
    times = []

    # Parse start/end time
    work_start_time = datetime.strptime(app.working_hours[0], time_format)
    work_end_time = datetime.strptime(app.working_hours[1], time_format)

    init_time = work_start_time

    while True:
        period_start = init_time
        period_end = period_start + timedelta(minutes=app.appointment_period)

        period = [
            period_start.strftime(time_format),
            period_end.strftime(time_format),
        ]
        times.append(period)

        if period_end.time() >= work_end_time.time():
            break

        init_time = period_end

    return times
