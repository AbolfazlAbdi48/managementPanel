from django.urls import path
from .views import (
    ProjectsListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    WorkDaysDetailView,
)

app_name = 'projects'
urlpatterns = [
    # projects
    path('', ProjectsListView.as_view(), name='list'),
    path('<pk>/<name>', ProjectDetailView.as_view(), name='detail'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('update/<pk>/<name>', ProjectUpdateView.as_view(), name='update'),
    path('delete/<pk>/<name>', ProjectDeleteView.as_view(), name='delete'),

    # work days
    path('work-day/<pk>/<name>', WorkDaysDetailView.as_view(), name='work-day-detail'),
]
