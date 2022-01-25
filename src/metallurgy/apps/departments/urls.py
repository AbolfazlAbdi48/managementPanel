from django.urls import path
from .views import (
    DepartmentsListView,
    DepartmentDetailView,
    DepartmentCreateView,
    DepartmentUpdateView,
    DepartmentDeleteView
)

app_name = 'departments'
urlpatterns = [
    path('', DepartmentsListView.as_view(), name='list'),
    path('<pk>/<name>', DepartmentDetailView.as_view(), name='detail'),
    path('create/', DepartmentCreateView.as_view(), name='create'),
    path('update/<pk>/<name>', DepartmentUpdateView.as_view(), name='update'),
    path('delete/<pk>/<name>', DepartmentDeleteView.as_view(), name='delete'),
]
