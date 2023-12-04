from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, RedirectView):
    url = "appointments/"
