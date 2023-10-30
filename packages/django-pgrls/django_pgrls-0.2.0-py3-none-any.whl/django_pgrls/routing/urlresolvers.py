import re
from typing import Any

from django.urls import URLResolver

from django_pgrls.state import get_current_tenant


class TenantPrefixPattern:
    converters: dict = {}

    @property
    def tenant_prefix(self) -> str:
        current_tenant = get_current_tenant()
        folder = getattr(current_tenant, "folder", None)
        return f"{folder}/" if folder else "/"

    @property
    def regex(self) -> re.Pattern:
        # This is only used by reverse() and cached in _reverse_dict.
        return re.compile(self.tenant_prefix)

    def match(self, path: str) -> tuple[str, tuple, dict] | None:
        tenant_prefix = self.tenant_prefix
        if path.startswith(tenant_prefix):
            return path[len(tenant_prefix) :], (), {}
        return None

    def check(self) -> list:
        return []

    def describe(self) -> str:
        return f"'{self}'"

    def __str__(self) -> str:
        return self.tenant_prefix


def tenant_patterns(*urls: object) -> list:
    """
    Add the tenant prefix to every URL pattern within this function.
    This may only be used in the root URLconf, not in an included URLconf.
    """
    return [URLResolver(TenantPrefixPattern(), list(urls))]


def get_dynamic_tenant_prefixed_urlconf(urlconf: str, dynamic_path: str) -> Any:
    """
    Generates a new URLConf module with all patterns prefixed with tenant.
    """
    from types import ModuleType

    from django.utils.module_loading import import_string

    class LazyURLConfModule(ModuleType):
        def __getattr__(self, attr: str) -> Any:
            imported = import_string(f"{urlconf}.{attr}")
            if attr == "urlpatterns":
                return tenant_patterns(*imported)
            return imported

    return LazyURLConfModule(dynamic_path)
