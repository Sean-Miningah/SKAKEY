# Generated by Django 4.0 on 2022-03-13 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_remove_shopkeeper_national_id_shop_confirmation_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPAuthentication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=40)),
            ],
        ),
    ]
