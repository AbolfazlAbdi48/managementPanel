from django.core import serializers
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import User, Customer, Employee

from .mixins import AuthenticatedMixin
from ..core.mixins import IsSuperUserMixin
from ..utils.character_generator import random_character_generator
from ..utils.sms_sender import send_single_sms

from .forms import (
    UserLoginForm,
    RegisterForm,
    AccountUpdateForm,
    AccountPasswordChangeForm,
    UserCreateForm
)
from ...envs.common import SMS_SETTINGS


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


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    def get_object(self, queryset=None):
        request = self.request
        return User.objects.get(pk=request.user.pk)

    template_name = 'registration/profile/profile_update.html'
    success_url = reverse_lazy('users:home')
    form_class = AccountUpdateForm


class AccountPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('users:home')
    template_name = 'registration/profile/profile_change_password.html'
    form_class = AccountPasswordChangeForm


class UserListView(IsSuperUserMixin, ListView):
    model = User
    ordering = ['-id']
    template_name = 'users/users_list.html'
    paginate_by = 12


@user_passes_test(lambda u: u.is_superuser)
def user_create_view(request):
    create_form = UserCreateForm(
        data=request.POST or None,
        initial={
            'bio': 'لطفا بیوگرافی خودرا ویرایش کنید'
        }
    )

    password = random_character_generator(8)

    if request.method == "POST":
        if create_form.is_valid():
            username = create_form.cleaned_data.get('username')
            email = create_form.cleaned_data.get('email')
            first_name = create_form.cleaned_data.get('first_name')
            last_name = create_form.cleaned_data.get('last_name')
            bio = create_form.cleaned_data.get('bio')
            status = create_form.cleaned_data.get('status')
            phone_number = create_form.cleaned_data.get('phone_number')

            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                bio=bio
            )
            user.set_password(password)

            if status == "staff":
                user.is_staff = True
                user.save()
            elif status == "customer":
                Customer.objects.create(account=user)
            elif status == "employee":
                Employee.objects.create(account=user)

            send_single_sms(
                message="کاربر جدید ایجاد شد \n"
                        f"نام کاربری: {user.username}\n"
                        f"رمز عبور: {password}\n"
                        f"ایمیل: {user.email}\n"
                        f"شماره تلفن: {user.phone_number}\n",
                receptor=SMS_SETTINGS['ADMIN_PHONE_NUMBER']
            )

            return redirect('users:users-list')

    context = {
        'default_password': password,
        'form': create_form
    }
    return render(request, 'users/users_create_update.html', context)
