from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import User

from .mixins import AuthenticatedMixin

from .forms import (
    UserLoginForm,
    RegisterForm,
    AccountUpdateForm
)


# Create your views here.
@login_required
def account_view(request):
    return render(request, 'registration/profile/profile_home.html')


class Login(AuthenticatedMixin, LoginView):
    authentication_form = UserLoginForm

    def get_success_url(self):
        return reverse('users:home')


class RegisterView(AuthenticatedMixin, CreateView):
    model = User
    success_url = reverse_lazy('login')
    form_class = RegisterForm
    template_name = 'registration/register.html'


class AccountUpdateView(UpdateView):
    def get_object(self, queryset=None):
        request = self.request
        return User.objects.get(pk=request.user.pk)

    template_name = 'registration/profile/profile_update.html'
    success_url = reverse_lazy('users:home')
    form_class = AccountUpdateForm
