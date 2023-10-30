import re
from typing import Callable, TypeAlias

from asgiref.sync import iscoroutinefunction, sync_to_async
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import clear_url_caches
from django.utils.decorators import sync_and_async_middleware

from django_pgrls.routing.urlresolvers import get_dynamic_tenant_prefixed_urlconf
from django_pgrls.state import activate
from django_pgrls.utils import get_domain_model, get_tenant_fk_field, remove_www


def strip_tenant_from_path_factory(prefix: str) -> Callable[[str], str]:
    def strip_tenant_from_path(path: str) -> str:
        return re.sub(r"^/{}/".format(prefix), "/", path)

    return strip_tenant_from_path


ResponseHandler: TypeAlias = Callable[[HttpRequest], HttpResponse]


@sync_and_async_middleware
def DomainRoutingMiddleware(get_response: ResponseHandler) -> ResponseHandler:
    """
    This middleware should be placed at the very top of the middleware stack.
    Selects the proper tenant using the request host.
    """

    def base_middleware(request: HttpRequest) -> HttpResponse | None:
        hostname = remove_www(request.get_host().split(":")[0])

        tenant = None

        ActualDomainModel = get_domain_model()
        prefix = request.path.split("/")[1]
        domain = None

        try:
            domain = ActualDomainModel._default_manager.select_related(get_tenant_fk_field()).get(
                domain=hostname, folder=prefix
            )
        except ActualDomainModel.DoesNotExist:
            try:
                domain = ActualDomainModel._default_manager.select_related(
                    get_tenant_fk_field()
                ).get(domain=hostname, folder="")
            except ActualDomainModel.DoesNotExist:
                pass

        if domain is not None:
            tenant = getattr(domain, get_tenant_fk_field())
            tenant.domain_url = hostname
            tenant.folder = None
            request.strip_tenant_from_path = lambda x: x

            if prefix and domain.folder == prefix:
                tenant.folder = prefix
                request.strip_tenant_from_path = strip_tenant_from_path_factory(prefix)
                clear_url_caches()  # Required to remove previous tenant prefix from cache
                dynamic_path = settings.ROOT_URLCONF + "_dynamically_tenant_prefixed"
                request.urlconf = get_dynamic_tenant_prefixed_urlconf(
                    settings.ROOT_URLCONF, dynamic_path
                )

            if domain.redirect_to_primary:
                primary_domain = tenant.domains.get(is_primary=True)
                path = request.strip_tenant_from_path(request.path)
                return redirect(primary_domain.absolute_url(path), permanent=True)

        # No tenant found from domain / folder
        if not tenant:
            raise Http404("No tenant for hostname '%s'" % hostname)

        request.tenant = tenant
        activate(tenant)

        return None

    if iscoroutinefunction(get_response):
        async_base_middleware = sync_to_async(base_middleware)

        async def middleware(request: HttpRequest) -> HttpResponse | None:
            if response := await async_base_middleware(request):
                return response

            return await get_response(request)

    else:

        def middleware(request: HttpRequest) -> HttpResponse | None:
            if response := base_middleware(request):
                return response

            return get_response(request)

    return middleware
