from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    account_view,
    RegisterView,
    AccountUpdateView,
    AccountPasswordChangeView,
    UserListView,
    user_create_view
)

app_name = 'users'
urlpatterns = [
    path('', account_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', AccountUpdateView.as_view(), name='update'),
    path('password-change/', AccountPasswordChangeView.as_view(), name='password-change'),

    path('users/', UserListView.as_view(), name='users-list'),
    path('users/create/', user_create_view, name='users-create'),
]
