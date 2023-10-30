from importlib import import_module

from django.conf import settings

BASE_BACKEND = "django.db.backends.postgresql"
ORIGINAL_BACKEND = getattr(settings, "PGRLS_ORIGINAL_BACKEND", BASE_BACKEND)

base_backend = import_module(BASE_BACKEND + ".base")
original_backend = import_module(ORIGINAL_BACKEND + ".base")
