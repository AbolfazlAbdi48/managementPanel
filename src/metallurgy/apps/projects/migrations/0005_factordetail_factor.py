# Generated by Django 4.0 on 2022-02-02 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_factordetail_factor'),
    ]

    operations = [
        migrations.AddField(
            model_name='factordetail',
            name='factor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='factor_details', to='projects.factor', verbose_name='فاکتور'),
            preserve_default=False,
        ),
    ]
