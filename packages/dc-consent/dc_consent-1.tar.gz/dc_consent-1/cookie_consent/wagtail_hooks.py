from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

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

from core.templatetags.scripts_tags import (
    css_hook_name,
    js_hook_name,
)
from wagtail import hooks

@hooks.register(css_hook_name)
def cookie_consent_css(context):
    return [
        "cookie_consent/cookie-consent.css",
    ]

@hooks.register(js_hook_name)
def cookie_consent_js(context):
    return [
        "cookie_consent/cookie-consent.js",
    ]
