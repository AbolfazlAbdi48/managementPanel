# Generated by Django 4.0 on 2022-01-25 20:43

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('departments', '0002_alter_department_staff_users'),
        ('users', '0007_alter_customer_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام پروژه')),
                ('description', models.TextField(verbose_name='توضیحات پروژه')),
                ('start_date', django_jalali.db.models.jDateField(verbose_name='تاریخ شروع')),
                ('end_date', django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ پایان')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customers', models.ManyToManyField(related_name='customers', to='users.Customer', verbose_name='کارفرمایان')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departments.department', verbose_name='دپارتمان مربوطه')),
            ],
            options={
                'verbose_name': 'پروژه',
                'verbose_name_plural': 'پروژه ها',
            },
        ),
    ]