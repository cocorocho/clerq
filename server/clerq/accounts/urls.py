from django.urls import path, include

from allauth.account.views import LoginView


urlpatterns = [
    path("signin/", LoginView.as_view(), name="account_signin"),
    path("", include("allauth.urls")),
]
