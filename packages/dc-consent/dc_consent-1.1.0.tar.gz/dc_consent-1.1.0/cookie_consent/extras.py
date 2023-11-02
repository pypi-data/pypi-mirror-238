from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail import hooks

class ModalExtra:
    def is_shown(self, request):
        return True

    def render(self, request, context):
        raise NotImplementedError()
    
class AnchorTagExtra(ModalExtra):
    get_url: callable  = None
    get_text: callable = None
    classes: str       = ""

    def __init__(self, get_url=None, get_text=None, classes=""):
        self.get_url  = get_url
        self.get_text = get_text
        self.classes  = classes

    def render(self, request, context):
        if callable(self.get_url):
            url = self.get_url(self.request)
        else:
            url = self.get_url

        if callable(self.get_text):
            text = self.get_text(self.request)
        else:
            text = self.get_text

        return mark_safe(f'<a href="{url}" class="{self.classes}">{text}</a>')
    
class RowModalExtra(ModalExtra):
    columns: list[ModalExtra] = []

    def render(self, request, context):
        return mark_safe(
            '<div class="row">' +
            "".join(
                f'<div class="col">{column.render(request, context)}</div>'
                for column in self.columns
            ) +
            '</div>'
        )
        


# We will check if wagtail is installed first; their hook system is simple; 
# and keeps everything centralized.
try:
    try:
        from wagtail.core import hooks
    except ImportError:
        from wagtail import hooks

    def get_cookie_modal_extras(request):
        return hooks.get_hooks("register_cookies_modal_extras")

except ImportError:
    # If wagtail is not installed, we will try to get the extras from the
    # django settings. The string defined in settings should point to a
    # callable that returns a list of ModalExtras, or a list of ModalExtras.
    from django.conf import settings
    from django.utils.module_loading import import_string

    try:
        _ = settings.COOKIE_CONSENT_EXTRAS
        def get_cookie_modal_extras(request):
            extras = getattr(settings, "COOKIE_CONSENT_EXTRAS", [])
            imported = import_string(extras)
            if callable(imported):
                return imported(request)
            return imported

    except AttributeError:
        def get_cookie_modal_extras(request):
            return []


