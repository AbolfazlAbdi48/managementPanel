from django import forms
from ..users.models import User
from .models import Department

staff_users = User.objects.filter(is_staff=True, is_superuser=False)
STAFF_USERS_CHOICES = tuple(
    [
        (user.id, user.username) for user in staff_users
    ]
)

class CreateUpdateDepartmentForm(forms.ModelForm):
    staff_users = forms.MultipleChoiceField(
        choices=STAFF_USERS_CHOICES,
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control form-control-lg form-control-solid'}
        ),
        required=False
    )

    class Meta:
        model = Department
        fields = ('name', 'staff_users', 'description')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'نام دپارتمان'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'توضیحات'
                }
            )
        }
