from django.urls import path
from .views import (
    DepartmentsListView
)

app_name = 'departments'
urlpatterns = [
    path('', DepartmentsListView.as_view(), name='list'),
]
