from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    account_view,
    RegisterView,
    AccountUpdateView
)

app_name = 'users'
urlpatterns = [
    path('', account_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', AccountUpdateView.as_view(), name='update'),
]
