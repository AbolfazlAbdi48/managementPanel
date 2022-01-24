from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Department
from .forms import CreateUpdateDepartmentForm
from ..core.mixins import IsSuperUserMixin


# Create your views here.
class DepartmentsListView(IsSuperUserMixin, ListView):
    """
    The view return all departments,
    only superuser can see this view.
    """

    model = Department
    ordering = ['-id']
    template_name = 'departments/departments_list.html'
    paginate_by = 12


class DepartmentDetailView(DetailView):
    """
    The view return department by pk,
    superuser and staff can see this view.
    """

    def get_object(self, queryset=None):
        department_pk = self.kwargs.get('pk')
        return Department.objects.filter(pk=department_pk).first()

    template_name = 'departments/department_detail.html'
    context_object_name = 'department'


class DepartmentCreateView(IsSuperUserMixin, CreateView):
    """
    The view create a new department,
    superuser only can work with this view.
    """

    model = Department
    template_name = 'departments/department_create_update.html'
    success_url = reverse_lazy('departments:list')
    form_class = CreateUpdateDepartmentForm


class DepartmentUpdateView(UpdateView):
    def get_object(self, queryset=None):
        department_pk = self.kwargs.get('pk')
        return Department.objects.filter(pk=department_pk).first()

    template_name = 'departments/department_create_update.html'
    success_url = reverse_lazy('departments:list')
    form_class = CreateUpdateDepartmentForm
