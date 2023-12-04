from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class LoginAndPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Composite mixin with both `LoginRequiredMixing` and `PermissionRequiredMixin`"""
