# Generated by Django 4.0 on 2022-02-04 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='ref_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]