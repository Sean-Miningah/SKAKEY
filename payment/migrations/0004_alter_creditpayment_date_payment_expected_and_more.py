# Generated by Django 4.0 on 2022-02-10 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_delete_payment_creditpayment_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditpayment',
            name='date_payment_expected',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='creditpayment',
            name='last_update',
            field=models.DateField(auto_now=True),
        ),
    ]
