from django.db import models
from django_jalali.db import models as jmodels
from ..departments.models import Department
from ..users.models import Customer
from ..utils.jalali_date import jalali_converter


# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام پروژه')
    description = models.TextField(verbose_name='توضیحات پروژه')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='دپارتمان مربوطه')
    customers = models.ManyToManyField(Customer, related_name='customers', verbose_name='کارفرمایان')
    start_date = jmodels.jDateField(verbose_name='تاریخ شروع')
    end_date = jmodels.jDateField(verbose_name='تاریخ پایان', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه ها'

    def __str__(self):
        return f"{self.name} -> {self.department.name}"

    def get_created_jalali(self):
        return jalali_converter(self.created)

    def get_updated_jalali(self):
        return jalali_converter(self.updated)

    def get_name_replace(self):
        return f"{self.name.replace(' ', '-')}"
