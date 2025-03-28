# Generated by Django 5.1.6 on 2025-03-07 17:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='username')),
                ('password', models.CharField(max_length=64, verbose_name='password')),
                ('equity', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='equity')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('ordertype', models.CharField(choices=[('1', 'Buy'), ('2', 'Sell')], max_length=64, verbose_name='order_type')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.users', verbose_name='user')),
            ],
        ),
    ]
