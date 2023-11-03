from django.template import Library, loader, Node, TemplateSyntaxError
from django.urls import reverse

register = Library()

from ..forms import (
    make_consent_form,
)

from ..options import (
    COOKIE_CONSENT_LOGO,
    COOKIE_CONSENT_LOGO_URL,
    COOKIE_CONSENT_TITLE,
    COOKIE_CONSENT_DESCRIPTION,
    COOKIE_CONSENT_BUTTON_ACCEPT,
    COOKIE_CONSENT_BUTTON_ACCEPT_ALL,
    COOKIE_CONSENT_BUTTON_DETAILS,
    COOKIE_CONSENT_BUTTON_SETTINGS,
    COOKIE_CONSENT_BUTTON_DECLINE,
)

from ..cookies import (
    ACCEPT_ALL_COOKIE,
)

from ..extras import (
    get_cookie_modal_extras,
)

from ..panels import (
    init_cookie_panels,
)

class CookieConsentNode(Node):
    def __init__(self, nodelist, args):
        self.nodelist = nodelist
        self.args = args
    
    def render(self, context):
        request = context["request"]
        args = []
        for arg in self.args:
            args.append(arg.resolve(context))

        if request.cookie_consent.allows(*args):
            return self.nodelist.render(context)
        
        return ""

@register.tag(name="consents_to")
def do_consents_to(parser, token):

    end_tag = "endconsents_to"
    args = []

    bits = token.split_contents()
    tag_name = bits.pop(0)

    if len(bits) < 1:
        raise TemplateSyntaxError(f"{tag_name} requires at least one argument")
    
    while len(bits) > 0:
        arg = bits.pop(0)
        if arg == "as":
            break

        compiled = parser.compile_filter(arg)
        args.append(compiled)

    nodelist = parser.parse((end_tag,))
    parser.delete_first_token()

    return CookieConsentNode(nodelist, args)

@register.simple_tag(takes_context=True)
def render_with_context(context, item):
    request = context["request"]
    if hasattr(item, "render"):
        return item.render(request, context)
    return item

@register.simple_tag(takes_context=True)
def cookie_consent(context):
    request = context["request"]

    action_url = reverse("cookie_consent:submit")
    policy_url = reverse("cookie_consent:policy")

    # if request.path.lower().strip("/") == policy_url.lower().strip("/"):
    #     return ""

    if not request.cookie_consent.submitted:
        cookie_panels = init_cookie_panels(request)
        cookie_form = make_consent_form(request, cookie_panels=cookie_panels)
        cookie_panels = [panel for panel in cookie_panels if panel.long_description]

        cookie_ctx = {
            "request": request,
            "parent_context": context,

            "cookie_modal_logo":        COOKIE_CONSENT_LOGO,
            "cookie_modal_logo_url":    COOKIE_CONSENT_LOGO_URL,
            "cookie_modal_title":       COOKIE_CONSENT_TITLE,
            "cookie_modal_description": COOKIE_CONSENT_DESCRIPTION,
            "cookie_modal_form_action": action_url,
            "cookie_modal_policy_url":  policy_url,
            "cookie_modal_form":        cookie_form,
            "cookie_modal_panels":      cookie_panels,
            "cookie_modal_extras":      get_cookie_modal_extras(request),

            "cookie_modal_accept_all_value": ACCEPT_ALL_COOKIE,

            "cookie_modal_button_accept":     COOKIE_CONSENT_BUTTON_ACCEPT,
            "cookie_modal_button_accept_all": COOKIE_CONSENT_BUTTON_ACCEPT_ALL,
            "cookie_modal_button_details":    COOKIE_CONSENT_BUTTON_DETAILS,
            "cookie_modal_button_settings":   COOKIE_CONSENT_BUTTON_SETTINGS,
            "cookie_modal_button_decline":    COOKIE_CONSENT_BUTTON_DECLINE,
        }

        template = loader.get_template("cookie_consent/cookie_modal.html")
        return template.render(cookie_ctx, request)

    return ""

