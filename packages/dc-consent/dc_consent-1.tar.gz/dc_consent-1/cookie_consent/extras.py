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
        
def get_cookie_modal_extras(request):
    return hooks.get_hooks("register_cookies_modal_extras")


