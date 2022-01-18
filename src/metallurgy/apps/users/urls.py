from django.urls import path
from .views import (
    account_view,
    RegisterView
)

app_name = 'users'
urlpatterns = [
    path('', account_view, name='home'),
    path('register/', RegisterView.as_view(), name='register')
]
