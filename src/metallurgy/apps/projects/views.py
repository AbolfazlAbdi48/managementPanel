from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProjectCreateUpdateForm
from .models import Project, WorkDay
from ..core.mixins import (
    IsSuperUserOrStaffUserMixin,
)
from .mixins import (
    ProjectDepartmentStaffUserMixin,
    ProjectCreateMixin,
    ProjectFormMixin,
    ProjectDetailMixin, WorkDayDetailMixin
)

# Create your views here.
from ..users.models import Customer


class ProjectsListView(IsSuperUserOrStaffUserMixin, ListView):
    """
    The view return projects for superuser and staff user.
    """

    def get_queryset(self):
        request = self.request
        if request.user.is_superuser:
            return Project.objects.all().order_by('-id')
        elif request.user.is_staff:
            return Project.objects.filter(department__staff_users__in=[request.user]).order_by('-id')

    template_name = 'projects/project_list.html'
    paginate_by = 12


class ProjectDetailView(ProjectDetailMixin, DetailView):
    """
    The view return a project detail.
    """

    def get_object(self, queryset=None):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # work days
        is_customer = Customer.objects.filter(account=self.request.user).exists()
        workdays = WorkDay.objects.filter(project=self.object).order_by('-id')
        if is_customer:
            workdays = WorkDay.objects.filter(
                project=self.object, accessibility__in=['only_customer', 'public']
            ).order_by('-id')
        context['workdays'] = workdays
        return context

    template_name = 'projects/project_detail.html'


class ProjectCreateView(ProjectCreateMixin, ProjectFormMixin, CreateView):
    """
    The view can create project,
    superuser and staff can create a project.
    """

    model = Project
    template_name = 'projects/project_create_update.html'
    form_class = ProjectCreateUpdateForm


class ProjectUpdateView(ProjectDepartmentStaffUserMixin, UpdateView):
    """
    The view can update a project,
    superuser and staff can update a project.
    """

    def get_object(self, queryset=None):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        return project

    template_name = 'projects/project_create_update.html'
    form_class = ProjectCreateUpdateForm


class ProjectDeleteView(ProjectDepartmentStaffUserMixin, DeleteView):
    """
    The for delete projects,
    only superuser and staff can work with this view.
    """

    def get_object(self, queryset=None):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        return project

    success_url = reverse_lazy('projects:list')
    template_name = 'projects/project_delete.html'


class WorkDaysDetailView(WorkDayDetailMixin, DetailView):
    """
    The view for work days detail.
    """

    def get_object(self, queryset=None):
        work_day_pk = self.kwargs.get('pk')
        work_day = get_object_or_404(WorkDay, pk=work_day_pk)
        return work_day

    template_name = 'work_days/work_days_detail.html'
