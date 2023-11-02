from typing import Any
from django import forms
from django.forms.widgets import Widget
from django.utils.translation import gettext_lazy as _

from .cookies import (
    ACCEPT_ALL_COOKIE,
    store_cookie_consent,
    set_cookie_consent_submitted,
)

from .panels import (
    init_cookie_panels,
    CookieConsentPanel,
)

class CookieConsentForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.all_accepted = False

    def full_clean(self) -> None:
        self.data = self.data.copy()
        for field, value in self.fields.items():
            if value.required:
                self.data[field] = "on"
    
        if ACCEPT_ALL_COOKIE in self.data:
            accept_all = self.data[ACCEPT_ALL_COOKIE]
            if accept_all.lower() == ACCEPT_ALL_COOKIE.lower():
                self.all_accepted = True
                
        super().full_clean()

    def save(self):
        print(self.cleaned_data)

        if self.all_accepted:
            for field in self.fields:
                store_cookie_consent(self.request, field, True)
        else:
            for field in self.fields:
                store_cookie_consent(self.request, field, self.cleaned_data[field])
        
        set_cookie_consent_submitted(self.request, True)
        self.request.session.modified = True
        return self.cleaned_data

class BooleanField(forms.BooleanField):
    def widget_attrs(self, widget: Widget) -> Any:
        if self.required:
            return {"disabled": ""}
        return {}
    
    def clean(self, value):
        if self.required:
            return True
        return super().clean(value)

def make_consent_form_class(cookie_panels: list[CookieConsentPanel]):
    fields = {
        panel.name: BooleanField(
            label=panel.title,
            required=panel.required,
            initial=panel.required or panel.initial,
            help_text=panel.description,
        )
        for panel in cookie_panels
    }

    return type("CookiePanelForm", (CookieConsentForm,), fields)

def make_consent_form(request, data=None):
    cookie_panels = init_cookie_panels(request)
    form_class = make_consent_form_class(cookie_panels)
    return form_class(request, data=data)
