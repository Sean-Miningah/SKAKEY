# Generated by Django 4.0 on 2022-02-28 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SubCounty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=40)),
                ('county', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcounty_county', to='shops.county')),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=40)),
                ('subcounty', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcounty_ward', to='shops.subcounty')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('start_date', models.DateField(auto_now=True)),
                ('email_address', models.CharField(max_length=50, unique=True)),
                ('photo', models.ImageField(upload_to='user/shop/')),
                ('category', models.CharField(max_length=20)),
                ('county', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='county', to='shops.county')),
                ('subcounty', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='subcounty', to='shops.subcounty')),
                ('ward', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ward', to='shops.ward')),
            ],
        ),
        migrations.CreateModel(
            name='ShopKeeper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('start_date', models.DateField(auto_now=True)),
                ('phone_number', models.CharField(max_length=50, unique=True)),
                ('passportnumber', models.CharField(blank=True, max_length=25)),
                ('is_employee', models.BooleanField(default=True)),
                ('national_id', models.CharField(blank=True, max_length=25)),
                ('firebase_token', models.CharField(blank=True, max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('shop', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.RESTRICT, related_name='shops', to='shops.shop')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
