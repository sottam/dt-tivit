# Generated by Django 5.1.3 on 2024-12-03 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=100)),
                ('user', models.ForeignKey(limit_choices_to={'user_type': 'admin'}, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='api.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(limit_choices_to={'user_type': 'user'}, on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='api.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
