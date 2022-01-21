from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.views.decorators.csrf import csrf_protect
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
    UserCreateForm,
    UserUpdateForm
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
    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by('-id')

    template_name = 'users/users_list.html'
    paginate_by = 12


class DeactivateUserListView(IsSuperUserMixin, ListView):
    def get_queryset(self):
        return User.objects.filter(is_active=False).order_by('-id')

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

            match status:
                case "staff":
                    user.is_staff = True
                    user.save()
                case "customer":
                    Customer.objects.create(account=user)
                case "employee":
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


@user_passes_test(lambda u: u.is_superuser)
def user_update_view(request, pk, username):
    user = get_object_or_404(User, pk=pk, username=username)
    user_status = 'superuser'

    match user:
        case user.is_staff:
            user_status = 'staff'
        case bool(user.employee):
            user_status = 'employee'
        case bool(user.customer):
            user_status = 'customer'

    update_form = UserUpdateForm(
        data=request.POST or None,
        initial={
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio
        }
    )

    if request.method == "POST":
        if update_form.is_valid():
            user.username = update_form.cleaned_data.get('username')
            user.email = update_form.cleaned_data.get('email')
            user.first_name = update_form.cleaned_data.get('first_name')
            user.last_name = update_form.cleaned_data.get('last_name')
            user.bio = update_form.cleaned_data.get('bio')
            user.phone_number = update_form.cleaned_data.get('phone_number')
            status = update_form.cleaned_data.get('status')

            if user_status != status:
                match status:
                    case "staff":
                        user.is_staff = True
                        user.save()
                    case "customer":
                        if bool(user.employee):
                            Employee.objects.get(account=user).delete()
                        elif user.is_staff:
                            user.is_staff = False
                            user.save()
                        Customer.objects.create(account=user)
                    case "employee":
                        if bool(user.customer):
                            Customer.objects.get(account=user).delete()
                        elif user.is_staff:
                            user.is_staff = False
                            user.save()
                        Employee.objects.create(account=user)

            return redirect('users:users-list')

    context = {
        'form': update_form,
        'user': user
    }
    return render(request, 'users/users_create_update.html', context)


class UserDetailView(IsSuperUserMixin, DetailView):
    model = User
    template_name = 'users/users_detail.html'


@user_passes_test(lambda u: u.is_superuser)
@csrf_protect
def users_activate_deactivate_view(request):
    user_pk = request.GET.get('pk')
    user = User.objects.filter(pk=user_pk).first()
    if user:
        match user.is_active:
            case True:
                user.is_active = False
            case False:
                user.is_active = True
        user.save()
        return JsonResponse(status=204, data={'message': 'deleted'})
    else:
        return JsonResponse(status=404, data={'message': 'user not found'})
