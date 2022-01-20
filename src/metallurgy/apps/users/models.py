import os
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from metallurgy.apps.utils.jalali_date import jalali_converter
from metallurgy.apps.utils.character_generator import random_character_generator


# Create your models here.
class User(AbstractUser):
    bio = models.TextField(verbose_name='بیوگرافی')
    phone_number = models.CharField(max_length=13, null=True, blank=True, verbose_name='شماره تلفن')

    def get_last_login_jalali(self):
        return jalali_converter(self.last_login)


class Employee(models.Model):
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
    account = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='اکانت مشتری')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'

    def __str__(self):
        return self.account.username
