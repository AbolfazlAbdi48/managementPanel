from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from .models import User

from .mixins import AuthenticatedMixin

from .forms import UserLoginForm, RegisterForm


# Create your views here.
@login_required
def account_view(request):
    return render(request, 'base/_Base.html')


class Login(AuthenticatedMixin, LoginView):
    authentication_form = UserLoginForm

    def get_success_url(self):
        return reverse('users:home')

class RegisterView(AuthenticatedMixin, CreateView):
    model = User
    success_url = reverse_lazy('login')
    form_class = RegisterForm
    template_name = 'registration/register.html'