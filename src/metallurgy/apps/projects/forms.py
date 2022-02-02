from django import forms
from .models import Project, WorkDay
from jalali_date.widgets import AdminJalaliDateWidget


class ProjectCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'نام پروژه'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'توضیحات',
                    'id': 'kt-ckeditor-1'
                }
            ),
            'department': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'دپارتمان',
                    'id': 'kt-ckeditor-1'
                }
            ),
            'customers': forms.SelectMultiple(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'کارفرمایان'
                }
            ),
            'accessibility': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'دسترسی ها'
                }
            ),
            'start_date': AdminJalaliDateWidget(
                attrs={
                    'autocomplete': 'off',
                },
            ),
            'end_date': AdminJalaliDateWidget(
                attrs={
                    'autocomplete': 'off',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].required = False


class WorkDayCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = WorkDay
        fields = '__all__'
        widgets = {
            'day': forms.Select(
                attrs={'class': 'form-control selectpicker'}
            ),
            'date': AdminJalaliDateWidget(
                attrs={'autocomplete': 'off',}
            ),
            'start_time': forms.TimeInput(
                attrs={'class': 'form-control'}
            ),
            'end_time': forms.TimeInput(
                attrs={'class': 'form-control'}
            ),
            'accessibility': forms.Select(
                attrs={'class': 'form-control selectpicker'}
            ),
            'employees': forms.SelectMultiple(
                attrs={'class': 'form-control'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].required = False
