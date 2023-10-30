from contextlib import contextmanager
from contextvars import ContextVar
from enum import Enum
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from django_pgrls.models import TenantModel  # pragma: no cover


class TenantConstraint(Enum):
    ALL = "__ALL__"
    NONE = "__NONE__"


active: ContextVar["TenantModel | TenantConstraint"] = ContextVar(
    "active", default=TenantConstraint.NONE
)


def get_current_tenant() -> "TenantModel | TenantConstraint":
    return active.get()


def activate(tenant: "TenantModel") -> None:
    active.set(tenant)


def deactivate() -> None:
    active.set(TenantConstraint.NONE)


@contextmanager
def bypass() -> Iterator[None]:
    token = active.set(TenantConstraint.ALL)

    yield

    active.reset(token)
