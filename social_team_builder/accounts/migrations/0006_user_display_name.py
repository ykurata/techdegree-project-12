# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-04 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='display_name',
            field=models.CharField(max_length=40, null=True, unique=True),
        ),
    ]
