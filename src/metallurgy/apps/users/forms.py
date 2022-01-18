from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django import forms
from .models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-solid h-auto py-7 px-6 rounded-lg',
                   'placeholder': 'نام کاربری'}
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-solid h-auto py-7 px-6 rounded-lg',
                'placeholder': 'کلمه عبور'
            }
        ))


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-solid h-auto py-7 px-6 rounded-lg font-size-h6',
                   'placeholder': 'نام کاربری'}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-solid h-auto py-7 px-6 rounded-lg font-size-h6',
                   'placeholder': 'ایمیل'}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-solid h-auto py-7 px-6 rounded-lg font-size-h6',
                   'placeholder': 'کلمه عبور'}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-solid h-auto py-7 px-6 rounded-lg font-size-h6',
                   'placeholder': ' تکرار کلمه عبور'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
