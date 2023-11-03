from django.apps import apps


def corptools_active() -> bool:
    return apps.is_installed("corptools")
