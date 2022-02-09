# Generated by Django 4.0 on 2022-02-09 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_creditpayment_paymentmethod'),
        ('shops', '0009_shoppingsession_payment_method_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.AddField(
            model_name='creditpayment',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shops.shoppingsession'),
        ),
    ]
