from django.urls import path
from .views import account_view

app_name = 'users'
urlpatterns = [
    path('', account_view, name='home')
]
