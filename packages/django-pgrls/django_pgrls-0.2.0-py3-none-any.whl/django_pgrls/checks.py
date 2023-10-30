from typing import Any

from django.core.checks import Error, Tags, register
from django.core.exceptions import ImproperlyConfigured
from django.db import connection

from django_pgrls.utils import get_domain_model, get_tenant_model


def user_is_superuser() -> bool:
    with connection.cursor() as cursor:
        cursor.execute("SELECT usesuper FROM pg_user WHERE usename = current_user;")
        return bool(list(cursor.fetchall())[0][0])


@register(Tags.database)
def check_database_user(app_configs: Any, **kwargs: Any) -> list[Error]:
    errors = []

    if user_is_superuser():
        errors.append(
            Error(
                "Database superuser will always bypass row level security",
                hint="Use a database user that has full privileges but is not superuser.",
                id="django_pgrls.E001",
            )
        )

    return errors


@register
def check_tenant_model(app_configs: Any, **kwargs: Any) -> list[Error]:
    from django_pgrls.models import TenantModel

    errors = []

    if not issubclass(get_tenant_model(), TenantModel):
        errors.append(
            Error(
                "Invalid TENANT_MODEL in settings",
                hint="Especify the model path (app.Model) of a model that inherits django_pgrls.TenantModel",
                id="django_pgrls.E002",
            )
        )

    return errors


@register
def check_domain_model(app_configs: Any, **kwargs: Any) -> list[Error]:
    from django_pgrls.routing.models import DomainModel

    errors = []

    try:
        ActualDomainModel = get_domain_model()
    except ImproperlyConfigured:
        pass
    else:
        if not issubclass(ActualDomainModel, DomainModel):
            errors.append(
                Error(
                    "Invalid DOMAIN_MODEL in settings",
                    hint="Especify the model path (app.Model) of a model that inherits django_pgrls.routing.DomainModel",
                    id="django_pgrls.E003",
                )
            )

    return errors
