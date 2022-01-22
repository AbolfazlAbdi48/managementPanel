from django.urls import path
from .views import (
    DepartmentsListView,
    DepartmentDetailView
)

app_name = 'departments'
urlpatterns = [
    path('', DepartmentsListView.as_view(), name='list'),
    path('<pk>/<name>', DepartmentDetailView.as_view(), name='detail'),
]
