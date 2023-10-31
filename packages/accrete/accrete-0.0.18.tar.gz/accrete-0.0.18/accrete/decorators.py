from functools import wraps

from django.shortcuts import redirect
from django.contrib.auth.views import login_required
from . import config


def tenant_required(
        redirect_field_name: str = None,
        login_url: str = None
):
    def decorator(f):
        @wraps(f)
        @login_required(
            redirect_field_name=redirect_field_name,
            login_url=login_url
        )
        def _wrapped_view(request, *args, **kwargs):
            tenant = request.tenant
            if not tenant:
                return redirect(config.ACCRETE_TENANT_NOT_SET_URL)
            return f(request, *args, **kwargs)
        return _wrapped_view
    return decorator
