# Generated by Django 4.0 on 2022-02-19 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreditPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='none', max_length=50)),
                ('number', models.CharField(max_length=15)),
                ('email', models.CharField(blank=True, max_length=40)),
                ('amount_payed', models.IntegerField()),
                ('total_shopping', models.IntegerField()),
                ('amount_remaining', models.IntegerField()),
                ('date_payment_expected', models.DateField()),
                ('last_update', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(default='CASH', max_length=50)),
            ],
        ),
    ]
