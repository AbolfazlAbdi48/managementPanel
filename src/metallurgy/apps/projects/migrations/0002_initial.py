# Generated by Django 4.0 on 2022-02-02 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('departments', '0002_initial'),
        ('projects', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workday',
            name='employees',
            field=models.ManyToManyField(to='users.Employee', verbose_name='کارمندان'),
        ),
        migrations.AddField(
            model_name='workday',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='پروژه'),
        ),
        migrations.AddField(
            model_name='project',
            name='customers',
            field=models.ManyToManyField(related_name='customers', to='users.Customer', verbose_name='کارفرمایان'),
        ),
        migrations.AddField(
            model_name='project',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departments.department', verbose_name='دپارتمان مربوطه'),
        ),
        migrations.AddField(
            model_name='factordetail',
            name='factor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factor_details', to='projects.factor', verbose_name='فاکتور'),
        ),
        migrations.AddField(
            model_name='factor',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factors', to='projects.project', verbose_name='پروژه'),
        ),
    ]
