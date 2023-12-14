import json

from django.forms.models import model_to_dict

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels import layers

from appointments.models import Appointment


class AppointmentConsumer(WebsocketConsumer):
    def connect(self):
        self.channel_layer_name = "appointments"

        async_to_sync(self.channel_layer.group_add)(
            self.channel_layer_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_layer_name,
            self.channel_name,
        )

    def receive(
        self, text_data: str | None = None, bytes_data: bytes | None = None
    ) -> str | None:
        try:
            data = json.loads(text_data)
        except json.decoder.JSONDecodeError:
            return

        event_type = data["HEADERS"].get("event-type")

        if event_type == "appointment_take":
            appointment_id = data.get("appointment")
            if appointment_id is None:
                return
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.takein_appointment(commit=True)

            response = {
                "event_type": event_type,
                "appointment": model_to_dict(
                    appointment,
                    fields=(
                        "id",
                        "subject",
                        "details",
                        "client_name",
                        "appointed_staff",
                    ),
                ),
            }
            self.send(json.dumps(response))

        # async_to_sync(self.channel_layer.group_send)(self.channel_layer_name, response)

    def appointment_takein_echo(self, event) -> None:
        EVENT_NAME = "appointment_take"

        # Appointment details
        appointment_id = event["appointment_id"]
        appointed_staff_id = event["appointed_staff_id"]

        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "event_type": EVENT_NAME,
                    "appointment_id": appointment_id,
                    "appointed_staff_id": appointed_staff_id,
                }
            )
        )

    def appointment_conclude_echo(self, event) -> None:
        EVENT_NAME = "appointment_conclude"

        # Appointment details
        appointment_id = event["appointment_id"]
        appointed_staff_id = event["appointed_staff_id"]

        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "event_type": EVENT_NAME,
                    "appointment_id": appointment_id,
                    "appointed_staff_id": appointed_staff_id,
                }
            )
        )

    @staticmethod
    def broadcast_appointment_takein(appointment: Appointment) -> None:
        """Broadcast event to all websocket clients after an appointment is taken in"""

        channel_layer = layers.get_channel_layer("default")
        async_to_sync(channel_layer.group_send)(
            "appointments",
            {
                "type": "appointment_takein_echo",
                "appointment_id": appointment.pk,
                "appointed_staff_id": appointment.appointed_staff.id,
            },
        )

    @staticmethod
    def broadcast_appointment_concluded(appointment: Appointment) -> None:
        """Broadcast event to all websocket clients after an event is concluded"""

        channel_layer = layers.get_channel_layer("default")
        async_to_sync(channel_layer.group_send)(
            "appointments",
            {
                "type": "appointment_conclude_echo",
                "appointment_id": appointment.pk,
                "appointed_staff_id": appointment.appointed_staff.id,
            },
        )
