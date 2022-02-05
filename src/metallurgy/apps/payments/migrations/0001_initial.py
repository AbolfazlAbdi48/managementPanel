# Generated by Django 4.0 on 2022-02-04 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='مبلغ پرداخت شده')),
                ('ref_id', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
                ('card_number', models.CharField(blank=True, max_length=18, null=True)),
                ('authority', models.CharField(blank=True, max_length=255, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('insert_date_time', models.DateTimeField(auto_now_add=True)),
                ('payment_date_time', models.DateTimeField(auto_now=True)),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='projects.factor', verbose_name='فاکتور')),
            ],
            options={
                'verbose_name': 'پرداخت',
                'verbose_name_plural': 'پرداخت ها',
            },
        ),
    ]