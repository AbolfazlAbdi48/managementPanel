from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectUpdateView
)

app_name = 'projects'
urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('update/<pk>/<name>', ProjectUpdateView.as_view(), name='update'),
]
