from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import ProjectCreateUpdateForm
from .models import Project
from ..core.mixins import (
    IsSuperUserOrStaffUserMixin,
    ProjectDepartmentStaffUserMixin,
    ProjectCreateMixin,
    ProjectFormMixin,
    ProjectDetailMixin
)


# Create your views here.

class ProjectsListView(IsSuperUserOrStaffUserMixin, ListView):
    def get_queryset(self):
        request = self.request
        if request.user.is_superuser:
            return Project.objects.all().order_by('-id')
        elif request.user.is_staff:
            return Project.objects.filter(department__staff_users__in=[request.user]).order_by('-id')

    template_name = 'projects/project_list.html'
    paginate_by = 12


class ProjectDetailView(ProjectDetailMixin, DetailView):
    def get_object(self, queryset=None):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        return project

    template_name = 'projects/project_detail.html'


class ProjectCreateView(ProjectCreateMixin, ProjectFormMixin, CreateView):
    """
    The view can create project,
    superuser and staff can create a project.
    """

    model = Project
    success_url = reverse_lazy('departments:list')
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

    success_url = reverse_lazy('departments:list')
    template_name = 'projects/project_create_update.html'
    form_class = ProjectCreateUpdateForm
