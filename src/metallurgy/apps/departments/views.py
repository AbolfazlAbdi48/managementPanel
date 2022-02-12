from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Department
from .forms import CreateUpdateDepartmentForm
from ..core.mixins import IsSuperUserMixin, IsSuperUserOrDepartmentStaffUserMixin
from ..projects.models import Project


# Create your views here.


class DepartmentsListView(ListView):
    """
    The view return all departments,
    only superuser can see this view.
    """

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_superuser:
            return Department.objects.all().order_by('-id')
        elif current_user.is_staff:
            return Department.objects.filter(staff_users__in=[current_user]).order_by('-id')
        else:
            raise Http404

    template_name = 'departments/departments_list.html'
    paginate_by = 12


class DepartmentDetailView(IsSuperUserOrDepartmentStaffUserMixin, DetailView):
    """
    The view return department by pk,
    superuser and staff can see this view.
    """

    def get_object(self, queryset=None):
        department_pk = self.kwargs.get('pk')
        department = get_object_or_404(Department, pk=department_pk)
        return department

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get projects
        projects = Project.objects.filter(department=self.object).order_by('-id')
        context['projects'] = projects
        return context

    template_name = 'departments/department_detail.html'
    context_object_name = 'department'


class DepartmentCreateView(IsSuperUserMixin, CreateView):
    """
    The view create a new department,
    superuser only can work with this view.
    """

    model = Department
    template_name = 'departments/department_create_update.html'
    form_class = CreateUpdateDepartmentForm


class DepartmentUpdateView(IsSuperUserOrDepartmentStaffUserMixin, UpdateView):
    """
    The view update a department.
    """

    def get_object(self, queryset=None):
        department_pk = self.kwargs.get('pk')
        department = get_object_or_404(Department, pk=department_pk)
        return department

    template_name = 'departments/department_create_update.html'
    form_class = CreateUpdateDepartmentForm


class DepartmentDeleteView(IsSuperUserOrDepartmentStaffUserMixin, DeleteView):
    """
    The view for delete department.
    """

    def get_object(self, queryset=None):
        department_pk = self.kwargs.get('pk')
        department = get_object_or_404(Department, pk=department_pk)
        return department

    template_name = 'departments/department_delete.html'
    success_url = reverse_lazy('departments:list')
