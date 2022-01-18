from django.urls import path
from .views import test

app_name = 'users'
urlpatterns = [
    path('', test)
]
