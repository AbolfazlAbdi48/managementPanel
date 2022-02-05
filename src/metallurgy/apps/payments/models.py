from django.db import models
from ..projects.models import Factor
from ..users.models import User
from ..utils.jalali_date import jalali_converter


# Create your models here.


class Payment(models.Model):
    factor = models.ForeignKey(
        Factor, on_delete=models.CASCADE, related_name='payments'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payments'
    )
    amount = models.BigIntegerField()
    ref_id = models.IntegerField(
        blank=True, null=True
    )
    status = models.BooleanField(default=False)
    card_number = models.CharField(
        max_length=18, blank=True, null=True
    )
    authority = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    message = models.TextField(
        blank=True, null=True
    )
    insert_date_time = models.DateTimeField(
        auto_now_add=True
    )
    payment_date_time = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'

    def __str__(self):
        return f"قیمت: {self.amount} | RefId : {self.ref_id}"

    def get_insert_date_jalali(self):
        return jalali_converter(self.insert_date_time)

    def get_payment_date_jalali(self):
        return jalali_converter(self.payment_date_time)
