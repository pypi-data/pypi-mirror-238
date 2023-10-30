from typing import Any, Iterable

from django.db import models, transaction

from django_pgrls.models import TenantModel
from django_pgrls.utils import get_domain_model, get_tenant_fk_field, get_tenant_model_path

fk_field = get_tenant_fk_field()


class DomainModelBase(models.base.ModelBase):
    def __new__(cls, name: str, bases: tuple, attrs: dict, **kwargs: object) -> Any:
        attrs[fk_field] = models.ForeignKey(
            get_tenant_model_path(),
            db_index=True,
            on_delete=models.CASCADE,
            related_name="domains",
        )

        return super().__new__(cls, name, bases, attrs, **kwargs)


class DomainModel(models.Model, metaclass=DomainModelBase):
    domain: Any = models.CharField(max_length=253, db_index=True)
    folder: Any = models.SlugField(max_length=253, blank=True, db_index=True)

    is_primary: Any = models.BooleanField(default=True)
    redirect_to_primary: Any = models.BooleanField(default=False)

    class Meta:
        abstract = True
        unique_together = (("domain", "folder"),)

    def __str__(self) -> str:
        return "/".join([self.domain, self.folder]) if self.folder else self.domain

    @transaction.atomic
    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        domain_list = self.__class__._default_manager.all()

        if using:
            domain_list = domain_list.using(using)

        domain_list = (
            domain_list.filter(**{fk_field: getattr(self, fk_field)})
            .filter(is_primary=True)
            .exclude(pk=self.pk)
        )

        self.is_primary = self.is_primary or (not domain_list.exists())

        if self.is_primary:
            domain_list.update(is_primary=False)
            if self.redirect_to_primary:
                self.redirect_to_primary = False

        super().save(force_insert, force_update, using, update_fields)

    def absolute_url(self, path: str) -> str:
        """
        Constructs an absolute url for this domain / folder and a given path
        """
        folder = self.folder and "/" + self.folder

        if not path.startswith("/"):
            path = "/" + path

        return "//" + self.domain + folder + path


def get_primary_domain_for_tenant(tenant: TenantModel) -> DomainModel | None:
    try:
        domain = tenant.domains.get(is_primary=True)
        return domain
    except get_domain_model().DoesNotExist:
        return None
