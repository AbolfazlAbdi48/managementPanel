from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import WorkDay, Factor
from ..departments.models import Department
from ..projects.models import Project


class ProjectAccessMixin:
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
        obj = get_object_or_404(Project, pk=pk)
        if request.user.is_staff and request.user in obj.department.staff_users.all() \
                or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        elif obj.accessibility == 'public' and request.user:
            return super().dispatch(request, *args, **kwargs)
        elif obj.accessibility == 'only_customer' \
                and obj.customers.filter(account=request.user).exists():
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class WorkDayDetailMixin:
    """
    it first check accessibility and then access.
    """

    def dispatch(self, request, pk, name, *args, **kwargs):
        obj = get_object_or_404(WorkDay, pk=pk)
        if request.user.is_staff and request.user in obj.project.department.staff_users.all() \
                or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        elif obj.accessibility == 'public' and request.user:
            return super().dispatch(request, *args, **kwargs)
        elif obj.accessibility == 'only_customer' \
                and obj.project.customers.filter(account=request.user).exists():
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class WorkDayCreateUpdateMixin:
    """
    The mixin set project field by project_pk for WorkDayCreateUpdateMixin.
    """

    def form_valid(self, form):
        project_pk = self.kwargs.get('project_pk')
        if project_pk:
            project = get_object_or_404(Project, pk=project_pk)
            self.obj = form.save(commit=False)
            self.obj.project = project
            self.obj.save()

        return super().form_valid(form)


class FactorAccessMixin:
    """
    The mixin for factor detail.
    """

    def dispatch(self, request, *args, **kwargs):
        factor_pk = self.kwargs.get('pk')
        obj = get_object_or_404(Factor, pk=factor_pk)
        if request.user.is_authenticated \
                and request.user in [customer.account for customer in obj.project.customers.all()] \
                or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404
