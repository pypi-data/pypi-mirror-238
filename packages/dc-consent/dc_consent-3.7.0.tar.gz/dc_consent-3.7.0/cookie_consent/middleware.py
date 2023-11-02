
from .cookies import (
    cookie_consent_submitted,
    has_consent,
)

class CookieConsent:

    def __init__(self, request):
        self.request = request

    def allows(self, *cookie_name):
        if not cookie_name:
            return False
        return has_consent(self.request, *cookie_name)
    
    @property
    def submitted(self):
        return cookie_consent_submitted(self.request)


class CookieConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.cookie_consent = CookieConsent(request)

        response = self.get_response(request)

        return response