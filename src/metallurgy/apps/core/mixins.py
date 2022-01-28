from django.http import Http404
from django.shortcuts import get_object_or_404
from ..departments.models import Department


class IsSuperUserMixin:
    """Check is superuser."""

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class IsSuperUserOrStaffUserMixin:
    """Check is superuser or staff user."""

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_staff or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class IsSuperUserOrDepartmentStaffUserMixin:
    """
    Check user is superuser or department staffuser.
    """

    def dispatch(self, request, pk, name, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        if request.user.is_authenticated \
                and request.user in department.staff_users.all() \
                or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404



