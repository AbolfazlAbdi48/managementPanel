from django.urls import path
from .views import (
    ProjectsListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView
)

app_name = 'projects'
urlpatterns = [
    path('', ProjectsListView.as_view(), name='list'),
    path('<pk>/<name>', ProjectDetailView.as_view(), name='detail'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('update/<pk>/<name>', ProjectUpdateView.as_view(), name='update'),
]
