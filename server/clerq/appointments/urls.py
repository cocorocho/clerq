from django.urls import path

from appointments.views import (
    AppointmentCreateView,
    AppointmentList,
    AppointmentDeleteView,
    AppointmentUpdateView,
    AppointmentDetailView,
    AppointmentConcludeView,
    take_in_appointment,
)


app_name = "appointments"

urlpatterns = [
    path("", AppointmentList.as_view(), name="appointment_list"),
    path("<int:pk>/", AppointmentDeleteView.as_view(), name="appointment_delete"),
    path(
        "<int:pk>/update/", AppointmentUpdateView.as_view(), name="appointment_update"
    ),
    path(
        "<int:pk>/details/", AppointmentDetailView.as_view(), name="appointment_details"
    ),
    path(
        "<int:appointment_id>/takein/", take_in_appointment, name="appointment_takein"
    ),
    path(
        "<int:pk>/conclude/",
        AppointmentConcludeView.as_view(),
        name="appointment_conclude",
    ),
    path("create/", AppointmentCreateView.as_view(), name="appointment_create"),
]
