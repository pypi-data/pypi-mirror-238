from django.shortcuts import render
from django.http import (
    JsonResponse,
    HttpResponseRedirect,
)
from .panels import (
    init_cookie_panels,
)
from .forms import (
    make_consent_form_class,
    set_cookie_consent_submitted,
)
from .cookies import (
    delete_cookie_consent,
)
from .options import (
    COOKIE_CONSENT_POLICY_PAGE_EXTENDS_FROM,
)

cookie_policy_panels = []

class CookiePolicyPanel:
    title: str = ""
    description: str = ""

    def __eq__(self, other):
        if isinstance(other, CookiePolicyPanel):
            return self.title == other.title
        elif isinstance(other, str):
            return self.title == other
        else:
            raise TypeError(f"Cannot compare {self.__class__.__name__} with {other.__class__.__name__}")

def register_cookie_policy_panel(panel: CookiePolicyPanel):
    cookie_policy_panels.append(panel)

def unregister_cookie_policy_panel(panel: CookiePolicyPanel):
    cookie_policy_panels.remove(panel)

def revoke_cookie_consent(request):
    set_cookie_consent_submitted(request, False)

    panels = init_cookie_panels(request)
    for panel in panels:
        delete_cookie_consent(request, panel.name)

    if "X-Requested-With" in request.headers:
        return JsonResponse(
            {
                "success": True, 
            }, 
            status=200
        )
    
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

def submit_cookie_consent_form(request):

    if not request.method == "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    panels = init_cookie_panels(request)
    form_cls = make_consent_form_class(panels)
    form = form_cls(request, request.POST)

    if not form.is_valid():
        return JsonResponse({"error": "Invalid form"}, status=400)
    
    form.save()

    if "X-Requested-With" in request.headers:
        return JsonResponse(
            {
                "success": True, 
            }, 
            status=200
        )
    
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

def policy(request):
    panels = init_cookie_panels(request)

    panels = [panel for panel in panels if panel.long_description]

    context = {
        "panels": panels,
        "extends_from": COOKIE_CONSENT_POLICY_PAGE_EXTENDS_FROM,
        "extra_panels": cookie_policy_panels,
    }

    return render(request, "cookie_consent/cookie_policy.html", context)