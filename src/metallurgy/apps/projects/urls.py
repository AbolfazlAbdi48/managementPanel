from django.urls import path
from .views import (
    ProjectsListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    WorkDayDetailView,
    WorkDayCreateView,
    WorkDayUpdateView,
)

app_name = 'projects'
urlpatterns = [
    # projects
    path('', ProjectsListView.as_view(), name='list'),
    path('<pk>/<name>', ProjectDetailView.as_view(), name='detail'),
    path('create', ProjectCreateView.as_view(), name='create'),
    path('update/<pk>/<name>', ProjectUpdateView.as_view(), name='update'),
    path('delete/<pk>/<name>', ProjectDeleteView.as_view(), name='delete'),

    # work days
    path('work-day/create/<project_pk>', WorkDayCreateView.as_view(), name='work-day-create'),
    path('work-day/<pk>/<name>', WorkDayDetailView.as_view(), name='work-day-detail'),
    path('work-day/update/<project_pk>/<pk>/<name>', WorkDayUpdateView.as_view(), name='work-day-update'),
]
