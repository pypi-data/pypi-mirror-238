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
    long_description = _(
        """Functional cookies are required for the website to function.
They are usually only set in response to actions made by you which amount to a request for services,
such as setting your privacy preferences, logging in or filling in forms.
You can set your browser to block or alert you about these cookies,
but some parts of the site will not then work.
These cookies do not store any personally identifiable information.
""")

class AnalyticsCookieConsentPanel(CookieConsentPanel):
    name        = "analytics"
    title       = _("Analytics cookies")
    description = _("This site uses analytics cookies to improve your experience.")
    required    = False
    long_description = _(
        """Analytics cookies allow us to count visits and traffic sources,
so we can measure and improve the performance of our site.
They help us know which pages are the most and least popular
and see how visitors move around the site.
All information these cookies collect is aggregated and therefore anonymous.
If you do not allow these cookies,
we will not know when you have visited our site.
""")
    

class MarketingCookieConsentPanel(CookieConsentPanel):
    name        = "marketing"
    title       = _("Marketing cookies")
    description = _("This site uses marketing cookies to improve your experience.")
    required    = False
    long_description = _(
        """Marketing cookies are used to track visitors across websites.
The intention is to display ads that are relevant and engaging for the individual user
and thereby more valuable for publishers and third party advertisers.
If you do not allow these cookies,
you will experience less targeted advertising.
""")
    

register_cookie_panel(FunctionalCookieConsentPanel, 0)
register_cookie_panel(AnalyticsCookieConsentPanel, 1)
register_cookie_panel(MarketingCookieConsentPanel, 2)

class CookieConsentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cookie_consent'
