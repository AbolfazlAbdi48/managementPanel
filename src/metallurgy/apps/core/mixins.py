from django.http import Http404
from django.shortcuts import get_object_or_404
from ..departments.models import Department
from ..projects.models import Project


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


class ProjectDepartmentStaffUserMixin:
    """
    Check user is superuser or project department staffuser.
    """

    def dispatch(self, request, pk, name, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        if request.user.is_authenticated \
                and request.user in project.department.staff_users.all() \
                or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class ProjectCreateMixin:
    """
    ...
    """

    def dispatch(self, request, *args, **kwargs):
        department_pk = request.GET.get('d_pk')

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if department_pk and request.user.is_staff:
            department = get_object_or_404(Department, pk=department_pk)
            if request.user in department.staff_users.all():
                return super().dispatch(request, *args, **kwargs)
        raise Http404


class ProjectFormMixin:
    """
    ...
    """

    def form_valid(self, form):
        d_pk = self.request.GET.get('d_pk')
        if d_pk:
            department = get_object_or_404(Department, pk=d_pk)
            self.obj = form.save(commit=False)
            self.obj.department = department
            self.obj.save()

        return super().form_valid(form)


class ProjectDetailMixin:
    """
    it first check accessibility and then return access.
    """

    def dispatch(self, request, pk, name, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        if request.user.is_staff and request.user in project.department.staff_users.all() \
                or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        elif project.accessibility == 'public' and request.user:
            return super().dispatch(request, *args, **kwargs)
        elif project.accessibility == 'only_customer' \
                and project.customers.filter(account=request.user).exists():
            return super().dispatch(request, *args, **kwargs)
        raise Http404
