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