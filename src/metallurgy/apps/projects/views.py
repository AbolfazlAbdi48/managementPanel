from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, modelformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import (
    ProjectCreateUpdateForm,
    WorkDayCreateUpdateForm,
    FactorForm,
    FactorDetailForm
)
from .models import Project, WorkDay, Factor, FactorDetail
from ..core.mixins import (
    IsSuperUserOrStaffUserMixin,
)
from .mixins import (
    ProjectDepartmentStaffUserMixin,
    ProjectCreateMixin,
    ProjectFormMixin,
    ProjectDetailMixin,
    WorkDayDetailMixin,
    WorkDayCreateUpdateMixin, FactorDetailAccessMixin
)
from ..users.models import Customer, Employee


# Create your views here.


class ProjectsListView(LoginRequiredMixin, ListView):
    """
    The view return projects for superuser and staff user.
    """

    def get_queryset(self):
        request = self.request
        is_customer = Customer.objects.filter(account=request.user).exists()
        is_employee = Employee.objects.filter(account=request.user).exists()

        if request.user.is_superuser:
            return Project.objects.all().order_by('-id')
        elif request.user.is_staff:
            return Project.objects.filter(department__staff_users__in=[request.user]).order_by('-id')
        elif is_customer:
            return Project.objects.filter(customers__in=[request.user.customer]).order_by('-id')
        elif is_employee:
            return Project.objects.filter(workday__employees__in=[request.user.employee]).order_by('-id').distinct()
        else:
            raise Http404

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


class WorkDayDetailView(WorkDayDetailMixin, DetailView):
    """
    The view for work days detail.
    """

    def get_object(self, queryset=None):
        work_day_pk = self.kwargs.get('pk')
        work_day = get_object_or_404(WorkDay, pk=work_day_pk)
        return work_day

    template_name = 'work_days/work_day_detail.html'


class WorkDayCreateView(IsSuperUserOrStaffUserMixin, WorkDayCreateUpdateMixin, CreateView):
    """
    The view for create a work day.
    """

    model = WorkDay
    template_name = 'work_days/work_day_create_update.html'
    form_class = WorkDayCreateUpdateForm


class WorkDayUpdateView(IsSuperUserOrStaffUserMixin, WorkDayCreateUpdateMixin, UpdateView):
    """
    The view for update work days.
    """

    def get_object(self, queryset=None):
        work_day_pk = self.kwargs.get('pk')
        work_day = get_object_or_404(WorkDay, pk=work_day_pk)
        return work_day

    template_name = 'work_days/work_day_create_update.html'
    form_class = WorkDayCreateUpdateForm


class WorkDayDeleteView(IsSuperUserOrStaffUserMixin, DeleteView):
    """
    The view for delete work days.
    """

    def get_object(self, queryset=None):
        work_day_pk = self.kwargs.get('pk')
        work_day = get_object_or_404(WorkDay, pk=work_day_pk)
        return work_day

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={
            'pk': self.object.project.id,
            'name': self.object.project.get_name_replace(),
        })

    template_name = 'work_days/work_day_delete.html'


class FactorDetailView(FactorDetailAccessMixin, DetailView):
    """
    The view for factor detail.
    """

    def get_object(self, queryset=None):
        factor_pk = self.kwargs.get('pk')
        factor = get_object_or_404(Factor, pk=factor_pk)
        return factor

    template_name = 'factors/factor_detail.html'


class PrintFactorDetailView(FactorDetailAccessMixin, DetailView):
    """
    The view for print factor detail.
    """

    def get_object(self, queryset=None):
        factor_pk = self.kwargs.get('pk')
        factor = get_object_or_404(Factor, pk=factor_pk)
        return factor

    template_name = 'factors/factor_print_detail.html'


def factor_create_view(request, *args, **kwargs):
    factor_form = FactorForm(request.POST or None)
    factor_detail_formset = formset_factory(FactorDetailForm, extra=1)
    formset = factor_detail_formset(request.POST or None)

    # get project
    project_pk = kwargs.get('project_pk')
    project = get_object_or_404(Project, pk=project_pk)

    if all([factor_form.is_valid(), formset.is_valid()]):
        factor = factor_form.save(commit=False)
        factor.project = project
        factor.save()
        for form in formset:
            factor_detail = form.save(commit=False)
            factor_detail.factor = factor
            factor_detail.save()

        return redirect(reverse_lazy('projects:factor-detail', kwargs={'project_pk': factor.pk, 'pk': factor.pk}))

    context = {
        'factor_form': factor_form,
        'factor_detail_formset': formset,
        'project': project,
        'form_length': 1
    }
    return render(request, 'factors/factor_create_update.html', context)


def factor_update_view(request, *args, **kwargs):
    # get factor
    factor = get_object_or_404(Factor, pk=kwargs.get('pk'))
    if factor.is_paid:
        raise Http404
    # get project
    project = get_object_or_404(Project, pk=kwargs.get('project_pk'))

    factor_form = FactorForm(request.POST or None, instance=factor)
    factor_detail_formset = modelformset_factory(
        FactorDetail, form=FactorDetailForm, extra=0, can_delete=True
    )
    qs = factor.factor_details.all()
    formset = factor_detail_formset(request.POST or None, queryset=qs)

    if all([factor_form.is_valid(), formset.is_valid()]):
        factor = factor_form.save(commit=False)
        factor.project = project
        factor.save()

        for form in formset:
            factor_detail = form.save(commit=False)
            factor_detail.factor = factor
            if form.cleaned_data['DELETE']:
                factor_detail.delete()
            else:
                factor_detail.save()

        return redirect(
            reverse_lazy(
                'projects:factor-detail',
                kwargs={'project_pk': factor.pk, 'pk': factor.pk}
            )
        )

    context = {
        'factor_form': factor_form,
        'factor_detail_formset': formset,
        'project': project,
        'factor': factor,
        'form_length': qs.count()
    }
    return render(request, 'factors/factor_create_update.html', context)


class FactorDeleteView(IsSuperUserOrStaffUserMixin, DeleteView):
    def get_object(self, queryset=None):
        factor_pk = self.kwargs.get('pk')
        factor = get_object_or_404(Factor, pk=factor_pk, is_paid=False)
        return factor

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={
            'pk': self.object.project.id,
            'name': self.object.project.get_name_replace(),
        })

    template_name = 'factors/factor_delete.html'
