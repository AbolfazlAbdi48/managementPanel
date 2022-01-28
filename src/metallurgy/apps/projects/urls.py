from django.urls import path
from .views import (
    ProjectsListView,
    ProjectCreateView,
    ProjectUpdateView
)

app_name = 'projects'
urlpatterns = [
    path('', ProjectsListView.as_view(), name='list'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('update/<pk>/<name>', ProjectUpdateView.as_view(), name='update'),
]
