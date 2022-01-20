from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
    UserCreationForm,
    PasswordChangeForm
)
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
    username = UsernameField(
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


class AccountPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password', 'class': 'form-control form-control-lg form-control-solid mb-2'
            }
        ),
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control form-control-lg form-control-solid mb-2'
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control form-control-lg form-control-solid mb-2'
            }
        ),
    )


class UserCreateForm(forms.Form):
    STATUS_CHOICES = (
        ('staff', 'ارشد'),
        ('employee', 'کارمند'),
        ('customer', 'کارفرما')
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-solid form-control-lg',
                'placeholder': 'نام کاربری'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-solid form-control-lg',
                'placeholder': 'ایمیل'
            }
        )
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-solid form-control-lg',
                'placeholder': 'نام'
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-solid form-control-lg',
                'placeholder': 'نام خانوادگی'
            }
        )
    )

    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control form-control-solid form-control-lg',
                'placeholder': 'بیوگرافی'
            }
        )
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-solid form-control-lg',
                'placeholder': 'شماره همراه'
            }
        )
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-lg form-control-solid'
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exist = User.objects.filter(username=username).exists()
        if is_exist:
            raise forms.ValidationError('نام کاربری از قبل وجود دارد')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exist = User.objects.filter(email=email).exists()
        if is_exist:
            raise forms.ValidationError('این ایمیل از قبل وجود دارد')

        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        is_exist = User.objects.filter(phone_number=phone_number).exists()
        if is_exist:
            raise forms.ValidationError('این شماره تلفن از قبل وجود دارد')

        return phone_number
