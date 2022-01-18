from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse

from .mixins import AuthenticatedMixin

from .forms import UserLoginForm


# Create your views here.
@login_required
def account_view(request):
    return render(request, 'base/_Base.html')


class Login(AuthenticatedMixin, LoginView):
    authentication_form = UserLoginForm

    def get_success_url(self):
        return reverse('users:home')
