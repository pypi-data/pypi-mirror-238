from typing import TYPE_CHECKING

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if TYPE_CHECKING:
    from django_pgrls.models import TenantModel
    from django_pgrls.routing.models import DomainModel


def get_tenant_model_path() -> str:
    "Returns the tenant model path."

    TENANT_MODEL = getattr(settings, "TENANT_MODEL", None)

    if TENANT_MODEL is None:
        raise ImproperlyConfigured("TENANT_MODEL not found in settings")

    return TENANT_MODEL


def get_tenant_fk_field() -> str:
    return get_tenant_model_path().split(".")[1].lower()


def get_tenant_model(require_ready: bool = True) -> type["TenantModel"]:
    "Returns the tenant model."

    TENANT_MODEL = getattr(settings, "TENANT_MODEL", None)

    if TENANT_MODEL is None:
        raise ImproperlyConfigured("TENANT_MODEL not found in settings")

    return apps.get_model(TENANT_MODEL, require_ready=require_ready)


def get_domain_model(require_ready: bool = True) -> type["DomainModel"]:
    "Returns the domain model."

    DOMAIN_MODEL = getattr(settings, "DOMAIN_MODEL", None)

    if DOMAIN_MODEL is None:
        raise ImproperlyConfigured("DOMAIN_MODEL not found in settings")

    return apps.get_model(DOMAIN_MODEL, require_ready=require_ready)


def remove_www(path: str) -> str:
    """
    Removes ``www``. from the beginning of the address. Only for
    routing purposes. ``www.test.com/login/`` and ``test.com/login/`` should
    find the same tenant.
    """
    if path.startswith("www."):
        return path[4:]
    return path
