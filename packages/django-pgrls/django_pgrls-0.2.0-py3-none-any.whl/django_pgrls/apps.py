from django.apps import AppConfig


class PgRlsConfig(AppConfig):
    name = "django_pgrls"

    def ready(self) -> None:
        from .checks import check_database_user, check_tenant_model  # noqa: F401
