
from django.urls import path
from .views import (
    submit_cookie_consent_form,
    revoke_cookie_consent,
)

app_name = "cookie_consent"

urlpatterns = [
    path("submit/", submit_cookie_consent_form, name="submit"),
    path("revoke/", revoke_cookie_consent, name="revoke")
]