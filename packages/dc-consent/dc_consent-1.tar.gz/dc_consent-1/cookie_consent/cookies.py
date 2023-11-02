ACCEPT_ALL_COOKIE = "cookie_consent_accept_all"
HAS_SUBMITTED_COOKIE = "cookie_consent_submitted"

def make_cookie_name(name: str):
    name = name.replace(" ", "_")
    name = name.replace("-", "_")
    name = name.lower()
    return f"cookie_consent_{name}"

def _is_true(value: str):
    if isinstance(value, bool):
        return value
    return value.lower() in ["true", "1", "yes", "on"]

def has_consent(request, *cookie_name):
    if not hasattr(request, "session"):
        return False

    consents = True

    for name in cookie_name:
        name = make_cookie_name(name)
        value = request.session.get(name, None)
        if value is None:
            return False
            
        consents = consents and _is_true(value)
        if not consents:
            return False
        
    return consents

def cookie_consent_submitted(request):
    if not hasattr(request, "session"):
        return False
    has_accepted_consent = request.session.get(HAS_SUBMITTED_COOKIE, None)
    if has_accepted_consent is None:
        return False
    
    return _is_true(has_accepted_consent)

def set_cookie_consent_submitted(request, value: bool):
    if not hasattr(request, "session"):
        return False
    request.session[HAS_SUBMITTED_COOKIE] = value

def store_cookie_consent(request, cookie_name, cookie_value):
    request.session[make_cookie_name(cookie_name)] = cookie_value

def delete_cookie_consent(request, cookie_name):
    if not hasattr(request, "session"):
        return False
    if cookie_name in request.session:
        del request.session[cookie_name]
