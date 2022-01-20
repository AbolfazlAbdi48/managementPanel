from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    account_view,
    RegisterView,
    AccountUpdateView,
    AccountPasswordChangeView,
    UserListView,
    DeactivateUserListView,
    user_create_view,
    UserDetailView,
    user_update_view,
    users_deactivate_view
)

app_name = 'users'
urlpatterns = [
    path('', account_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', AccountUpdateView.as_view(), name='update'),
    path('password-change/', AccountPasswordChangeView.as_view(), name='password-change'),

    path('users/', UserListView.as_view(), name='users-list'),
    path('users/deactivated/', DeactivateUserListView.as_view(), name='users-deactivate-list'),
    path('users/create/', user_create_view, name='users-create'),
    path('users/<pk>/<username>', UserDetailView.as_view(), name='users-detail'),
    path('users/update/<pk>/<username>', user_update_view, name='users-update'),
    path('users/deactivate/', users_deactivate_view, name='users-deactivate'),
]
