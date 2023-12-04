from django.urls import path

from appointments.views import (
    AppointmentCreateView,
    AppointmentList,
    AppointmentDeleteView,
    AppointmentUpdateView,
    AppointmentDetailView,
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
    path("create/", AppointmentCreateView.as_view(), name="appointment_create"),
]
