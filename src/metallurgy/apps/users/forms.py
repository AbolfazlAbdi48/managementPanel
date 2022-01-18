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

    first_name = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-solid h-auto py-7 px-6 rounded-lg font-size-h6',
                   'placeholder': 'نام'}
        )
    )

    last_name = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-solid h-auto py-7 px-6 rounded-lg font-size-h6',
                   'placeholder': 'نام خانوادگی'}
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
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class AccountUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg form-control-solid',
                   'placeholder': 'نام کاربری'}
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-lg form-control-solid',
                   'placeholder': 'ایمیل'}
        ),
        disabled='disable'
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg form-control-solid',
                   'placeholder': 'نام'}
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg form-control-solid',
                   'placeholder': 'نام خانوادگی'}
        )
    )

    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control form-control-lg form-control-solid',
                   'placeholder': 'بیوگرافی'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'bio')
