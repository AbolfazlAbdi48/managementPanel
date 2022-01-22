from django.views.generic import ListView
from .models import Department
from ..core.mixins import IsSuperUserMixin


# Create your views here.
class DepartmentsListView(IsSuperUserMixin, ListView):
    """
    The view return all departments,
    only superuser can see this view.
    """
    model = Department
    template_name = 'departments/departments_list.html'
    paginate_by = 12
