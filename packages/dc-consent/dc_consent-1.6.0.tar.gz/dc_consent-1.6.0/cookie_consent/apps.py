from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .panels import (
    CookieConsentPanel,
    register_cookie_panel,
)

class FunctionalCookieConsentPanel(CookieConsentPanel):
    name        = "functional"
    title       = _("Functional cookies")
    description = _("These cookies are required for the website to function.")
    required    = True

class AnalyticsCookieConsentPanel(CookieConsentPanel):
    name        = "analytics"
    title       = _("Analytics cookies")
    description = _("This site uses analytics cookies to improve your experience.")
    required    = False

class MarketingCookieConsentPanel(CookieConsentPanel):
    name        = "marketing"
    title       = _("Marketing cookies")
    description = _("This site uses marketing cookies to improve your experience.")
    required    = False

register_cookie_panel(FunctionalCookieConsentPanel, 0)
register_cookie_panel(AnalyticsCookieConsentPanel, 1)
register_cookie_panel(MarketingCookieConsentPanel, 2)

class CookieConsentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cookie_consent'
