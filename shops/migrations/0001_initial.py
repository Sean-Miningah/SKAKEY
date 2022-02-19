# Generated by Django 4.0 on 2022-02-19 01:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now, max_length=50)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('email_address', models.CharField(max_length=15, unique=True)),
                ('photo', models.ImageField(upload_to='user/shop/')),
                ('category', models.CharField(max_length=20)),
                ('county', models.CharField(max_length=100)),
                ('ward', models.CharField(max_length=100)),
                ('subcounty', models.CharField(max_length=100)),
                ('firebase_token', models.CharField(blank=True, max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.BigIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('mode_of_payment', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='payment', to='payment.paymentmethod')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('p_description', models.TextField(max_length=500)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shop')),
            ],
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('price', models.BigIntegerField()),
                ('p_description', models.TextField(max_length=250)),
                ('source', models.CharField(blank=True, max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(blank=True, upload_to='Shop/ShopProduct/')),
                ('barcode', models.CharField(blank=True, max_length=150)),
                ('minimum_stock_level', models.BigIntegerField(default=0)),
                ('reorder_quantity', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.productcategory')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shop')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('total', models.BigIntegerField(null=True)),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='payment.paymentmethod')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shop')),
            ],
        ),
        migrations.CreateModel(
            name='ShopKeeper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=50, unique=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now, max_length=50)),
                ('national_id', models.CharField(blank=True, max_length=25)),
                ('passportnumber', models.CharField(blank=True, max_length=25)),
                ('is_employee', models.BooleanField(default=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shop')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.BigIntegerField()),
                ('total_price', models.BigIntegerField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shops.shopproduct')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shops.shoppingsession'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shops.shop'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.BigIntegerField()),
                ('price', models.BigIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shops.shopproduct')),
                ('session', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shops.shoppingsession')),
            ],
        ),
    ]
