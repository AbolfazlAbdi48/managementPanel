# Generated by Django 4.0 on 2022-02-04 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('projects', '0002_initial'),
        ('payments', '0003_alter_payment_authority'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='users.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='factor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='projects.factor'),
        ),
    ]
