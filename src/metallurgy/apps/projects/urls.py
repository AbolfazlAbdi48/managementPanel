from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    # projects
    path('', views.ProjectsListView.as_view(), name='list'),
    path('<pk>/<name>', views.ProjectDetailView.as_view(), name='detail'),
    path('create', views.ProjectCreateView.as_view(), name='create'),
    path('update/<pk>/<name>', views.ProjectUpdateView.as_view(), name='update'),
    path('delete/<pk>/<name>', views.ProjectDeleteView.as_view(), name='delete'),

    # work days
    path('work-day/create/<project_pk>', views.WorkDayCreateView.as_view(), name='work-day-create'),
    path('work-day/<pk>/<name>', views.WorkDayDetailView.as_view(), name='work-day-detail'),
    path('work-day/update/<project_pk>/<pk>/<name>', views.WorkDayUpdateView.as_view(), name='work-day-update'),
    path('work-day/delete/<pk>/<name>', views.WorkDayDeleteView.as_view(), name='work-day-delete'),

    # factors
    path('factor/create/<project_pk>', views.factor_create_view, name='factor-create'),
    path('factor/<project_pk>/<pk>', views.FactorDetailView.as_view(), name='factor-detail'),
    path('factor/print/<project_pk>/<pk>', views.PrintFactorDetailView.as_view(), name='factor-print-detail'),
]
