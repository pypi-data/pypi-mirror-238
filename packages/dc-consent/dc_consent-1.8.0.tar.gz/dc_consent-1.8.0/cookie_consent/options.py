from django.conf import settings
from django.utils.translation import gettext_lazy as _

COOKIE_CONSENT_TITLE = getattr(settings, "COOKIE_CONSENT_TITLE", _("Cookies"))
COOKIE_CONSENT_DESCRIPTION = getattr(settings, "COOKIE_CONSENT_DESCRIPTION", _("This site uses cookies to improve your experience."))
COOKIE_CONSENT_BUTTON_ACCEPT = getattr(settings, "COOKIE_CONSENT_BUTTON_ACCEPT", _("Accept"))
COOKIE_CONSENT_BUTTON_ACCEPT_ALL = getattr(settings, "COOKIE_CONSENT_BUTTON_ACCEPT_ALL", _("Accept All"))
COOKIE_CONSENT_BUTTON_DECLINE = getattr(settings, "COOKIE_CONSENT_BUTTON_DECLINE", _("Decline"))
COOKIE_CONSENT_BUTTON_SETTINGS = getattr(settings, "COOKIE_CONSENT_BUTTON_SETTINGS", _("Settings"))
COOKIE_CONSENT_POLICY_PAGE_EXTENDS_FROM = getattr(settings, "COOKIE_CONSENT_POLICY_PAGE_EXTENDS_FROM", "base.html")

