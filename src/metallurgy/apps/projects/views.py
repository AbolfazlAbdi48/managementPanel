from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Project

# Create your views here.


class ProjectCreateView(CreateView):
    """
    The view can create project,
    """

