from django.urls import path

from appointments.consumers import AppointmentConsumer


websocket_urlpatterns = [
    path("appointments/ws/", AppointmentConsumer.as_asgi(), name="ws"),
]
