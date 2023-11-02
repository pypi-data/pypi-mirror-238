from django.conf import settings
from django.utils.translation import gettext_lazy as _
import os

COOKIE_CONSENT_LOGO = getattr(settings, "COOKIE_CONSENT_LOGO", "cookie_consent/img/ga-logo.svg")
COOKIE_CONSENT_LOGO_URL = getattr(settings, "COOKIE_CONSENT_LOGO_URL", "https://goodadvice.it")
COOKIE_CONSENT_TITLE = getattr(settings, "COOKIE_CONSENT_TITLE", _("Cookies"))
COOKIE_CONSENT_DESCRIPTION = getattr(settings, "COOKIE_CONSENT_DESCRIPTION", _("This site uses cookies to improve your experience."))
COOKIE_CONSENT_BUTTON_ACCEPT = getattr(settings, "COOKIE_CONSENT_BUTTON_ACCEPT", _("Accept"))
COOKIE_CONSENT_BUTTON_ACCEPT_ALL = getattr(settings, "COOKIE_CONSENT_BUTTON_ACCEPT_ALL", _("Accept All"))
COOKIE_CONSENT_BUTTON_DECLINE = getattr(settings, "COOKIE_CONSENT_BUTTON_DECLINE", _("Decline"))
COOKIE_CONSENT_BUTTON_DETAILS = getattr(settings, "COOKIE_CONSENT_BUTTON_DETAILS", _("Details"))
COOKIE_CONSENT_BUTTON_SETTINGS = getattr(settings, "COOKIE_CONSENT_BUTTON_SETTINGS", _("Settings"))
COOKIE_CONSENT_POLICY_PAGE_EXTENDS_FROM = getattr(settings, "COOKIE_CONSENT_POLICY_PAGE_EXTENDS_FROM", "base.html")

