import os
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from metallurgy.apps.utils.jalali_date import jalali_converter
from metallurgy.apps.utils.character_generator import random_character_generator


# Create your models here.
class User(AbstractUser):
    """
    Customize user model.
    """
    bio = models.TextField(verbose_name='بیوگرافی')
    phone_number = models.CharField(max_length=13, null=True, blank=True, verbose_name='شماره تلفن')
    last_activity = models.DateTimeField(null=True, blank=True, verbose_name='آخرین فعالیت')

    def get_last_login_jalali(self):
        return jalali_converter(self.last_login)

    def get_last_activity_jalali(self):
        return jalali_converter(self.last_activity)


class Employee(models.Model):
    """
    The main model of the employee,
    One-To-One relationship with User model.
    """
    account = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='اکانت کارمند')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندان'

    def __str__(self):
        return self.account.username


class Customer(models.Model):
    """
    The main model of the customer,
    One-To-One relationship with User model.
    """
    account = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='اکانت مشتری')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'کارفرما'
        verbose_name_plural = 'کارفرمایان'

    def __str__(self):
        return self.account.username
