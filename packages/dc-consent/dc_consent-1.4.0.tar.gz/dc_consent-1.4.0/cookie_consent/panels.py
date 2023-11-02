from django.utils.translation import gettext_lazy as _
import copy

def make_name(name: str):
    name = name.replace(" ", "_")
    name = name.replace("-", "_")
    name = name.lower()
    return name

class CookieConsentPanelMeta(type):
    def __new__(cls, name, bases, attrs):

        if attrs.get("abstract", False):
            return super().__new__(cls, name, bases, attrs)
        
        if "name" not in attrs:
            attrs["name"] = make_name(name)
        
        return super().__new__(cls, name, bases, attrs)

class CookieConsentPanel(metaclass=CookieConsentPanelMeta):
    abstract    = True
    name        = None
    title       = None
    description = None
    # Is the field required?
    required    = False
    # Will always be true if the field is required.
    initial     = False

    def __init__(self, request):
        self.request = request

    def __eq__(self, other: "CookieConsentPanel"):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, CookieConsentPanel):
            return self.name == other.name
        else:
            raise TypeError(f"Cannot compare {self.__class__.__name__} with {other.__class__.__name__}")

cookie_registry: dict[str, CookieConsentPanel] = {}

class RegisteredPanel:
    def __init__(self, panel: CookieConsentPanel, order: int):
        self.panel = panel
        self.order = order

    def __eq__(self, other: "RegisteredPanel"):
        if isinstance(other, RegisteredPanel):
            return self.panel.name == other.panel.name
        elif isinstance(other, CookieConsentPanel) or (type(other) == type and issubclass(other, CookieConsentPanel)):
            return self.panel.name == other.name
        else:
            raise TypeError(f"Cannot compare {self.__class__.__name__} with {other.__class__.__name__}")
    
    def __lt__(self, other: "RegisteredPanel"):
        if isinstance(other, RegisteredPanel):
            return self.order < other.order
        return self.order < other
    
    def __gt__(self, other: "RegisteredPanel"):
        if isinstance(other, RegisteredPanel):
            return self.order > other.order
        return self.order > other

def register_cookie_panel(panel: CookieConsentPanel=None, order: int = 0):
    if panel is None:
        return lambda panel: register_cookie_panel(panel, order)
    
    if not issubclass(panel, CookieConsentPanel):
        raise TypeError(f"Expected CookieConsentPanel, got {panel.__class__.__name__}")
    
    if panel.name in cookie_registry:
        # remove the panel to change the order
        del cookie_registry[panel.name]
    
    cookie_registry[panel.name] = RegisteredPanel(panel, order)

def unregister_cookie_panel(panel: CookieConsentPanel):
    name = panel
    if hasattr(panel, "name"):
        name = panel.name

    if name in cookie_registry:
        del cookie_registry[name]

def get_cookie_panels(order=True):
    panels: list[RegisteredPanel] = copy.deepcopy(list(cookie_registry.values()))

    if order:
        # Sort by registered panels.
        panels.sort()

    for panel in panels:
        # Yield the actual panel.
        yield panel.panel

def init_cookie_panels(request):
    cookie_panels = get_cookie_panels()
    cookie_panels = [panel(request) for panel in cookie_panels]
    return cookie_panels

