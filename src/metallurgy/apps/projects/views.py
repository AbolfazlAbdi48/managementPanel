from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import ProjectCreateUpdateForm
from .models import Project
from ..core.mixins import (
    IsSuperUserMixin,
    ProjectDepartmentStaffUserMixin,
    ProjectCreateMixin,
    ProjectFormMixin
)

# Create your views here.
from ..departments.models import Department


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
