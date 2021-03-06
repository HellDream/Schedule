# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-14 11:22
from __future__ import unicode_literals

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(blank=True, default='', max_length=120)),
                ('school', models.CharField(blank=True, max_length=200, null=True)),
                ('user_stu_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=11)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=accounts.models.upload_location)),
                ('description', models.TextField(blank=True, default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
