import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    now_time = timezone.now()
    final_name = f"{instance.id}_{instance.username}_{now_time}{ext}"
    return f"users/profile_images/{final_name}"


# Create your models here.
class User(AbstractUser):
    bio = models.TextField(verbose_name='بیوگرافی')


class Employee(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='اکانت کارمند')
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن کارمند')
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
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن مشتری')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'

    def __str__(self):
        return self.account.username
