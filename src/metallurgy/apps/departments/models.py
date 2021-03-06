from django.db import models
from django.urls import reverse

from ..users.models import User


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام دپارتمان')
    staff_users = models.ManyToManyField(
        User, related_name='staff_users', blank=True, verbose_name='کاربران ارشد'
    )
    description = models.TextField(verbose_name='توضیحات دپارتمان')

    class Meta:
        verbose_name = 'دپارتمان'
        verbose_name_plural = 'دپارتمان ها'

    def __str__(self):
        return f"{self.name} | {self.description}"

    def get_name_replace(self):
        return f"{self.name.replace(' ', '-')}"

    def get_absolute_url(self):
        return reverse('departments:detail', kwargs={'pk': self.pk, 'name': self.get_name_replace()})
