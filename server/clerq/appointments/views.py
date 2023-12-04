from typing import Any

from django.utils.timezone import now
from django.db.models import QuerySet
from django.forms.models import BaseModelForm
from django.views.generic import CreateView, ListView, View, UpdateView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse

from core.base.auth.mixins import LoginAndPermissionRequiredMixin
from appointments.forms import AppointmentForm
from appointments.models import Appointment


class AppointmentDeleteView(LoginAndPermissionRequiredMixin, View):
    """Delete appointment by setting `is_canceled` attr `True`"""

    permission_required = ("appointments.delete_appointment",)

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Cancel Appointment"""
        appointment = get_object_or_404(
            Appointment.objects.filter(is_canceled=False), pk=pk
        )
        appointment.is_canceled = True
        appointment.save()

        return HttpResponse(status=200)


class AppointmentUpdateView(LoginAndPermissionRequiredMixin, UpdateView):
    """Update appointment"""

    permission_required = ("appointments.change_appointment",)
    form_class = AppointmentForm
    template_name = "appointments/forms/appointment.html"
    success_url = reverse_lazy("appointments:appointment_list")

    def get_queryset(self) -> QuerySet[Appointment]:
        return Appointment.objects.select_related("appointed_staff")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["operation"] = "update"
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Return 200 after update success"""

        response = super().post(request, *args, **kwargs)
        response.status_code = 200
        return response


class AppointmentDetailView(LoginAndPermissionRequiredMixin, DetailView):
    """Get appointment details"""

    permission_required = ("appointments.view_appointment",)

    def get_queryset(self) -> QuerySet[Appointment]:
        return Appointment.objects.select_related("appointed_staff")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = AppointmentForm(
            instance=context["object"], disable_fields=False
        )
        return context


class AppointmentList(LoginAndPermissionRequiredMixin, ListView):
    """Get appointments - paginated"""

    paginate_by = 25
    template_name = "appointments/appointment_list.html"
    permission_required = ("appointments.view_appointment",)
    queryset = Appointment.objects.select_related("appointed_staff").filter(
        is_canceled=False
    )


class AppointmentCreateView(LoginAndPermissionRequiredMixin, CreateView):
    """Create new appointment"""

    permission_required = ("appointments.add_appointment",)
    template_name = "appointments/forms/appointment.html"
    form_class = AppointmentForm
    success_url = reverse_lazy("appointments:appointment_create")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.appointer_staff = self.request.user
        super().form_valid(form)
        return HttpResponse(status=201)

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = {
            "appointment_date": now().date().strftime("%Y-%m-%d"),
        }
        return kwargs
