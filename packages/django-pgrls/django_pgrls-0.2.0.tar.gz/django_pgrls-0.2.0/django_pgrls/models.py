from typing import Any, Iterable

from asgiref.sync import sync_to_async
from django.db import models

from django_pgrls.constraints import RowLevelSecurityConstraint
from django_pgrls.managers import TenantBoundManager, TenantBypassManager
from django_pgrls.state import TenantConstraint, activate, deactivate, get_current_tenant
from django_pgrls.utils import get_tenant_fk_field, get_tenant_model_path


class TenantModel(models.Model):
    class Meta:
        abstract = True

    def __enter__(self) -> None:
        self._previous_tenant = get_current_tenant()
        if self._previous_tenant is not TenantConstraint.ALL:
            activate(self)

    __aenter__ = sync_to_async(__enter__)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        _previous_tenant = getattr(self, "_previous_tenant", TenantConstraint.NONE)
        if _previous_tenant is TenantConstraint.NONE:
            deactivate()
        elif _previous_tenant is not TenantConstraint.ALL:
            activate(_previous_tenant)

    __aexit__ = sync_to_async(__exit__)


fk_field = get_tenant_fk_field()


class TenantBoundBase(models.base.ModelBase):
    def __new__(cls, name: str, bases: tuple, attrs: dict, **kwargs: object) -> Any:
        attrs[fk_field] = models.ForeignKey(
            get_tenant_model_path(),
            on_delete=models.CASCADE,
            related_name="+",
        )

        if "Meta" in attrs:
            constraints = getattr(attrs["Meta"], "constraints", [])
            if not any(
                type(constraint) is RowLevelSecurityConstraint for constraint in constraints
            ):
                constraints.append(RowLevelSecurityConstraint(fk_field))
                setattr(attrs["Meta"], "constraints", constraints)

        return super().__new__(cls, name, bases, attrs, **kwargs)


class TenantBoundModel(models.Model, metaclass=TenantBoundBase):
    objects = TenantBoundManager()
    unbound_objects = TenantBypassManager()

    class Meta:
        abstract = True
        constraints = [
            RowLevelSecurityConstraint(fk_field),
        ]

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if getattr(self, fk_field, None) is None:
            current_tenant = get_current_tenant()
            if type(current_tenant) is not TenantConstraint:
                setattr(self, fk_field, current_tenant)

        super().save(force_insert, force_update, using, update_fields)
