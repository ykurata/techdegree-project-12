# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-21 05:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0018_auto_20181120_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='applicants',
            field=models.ManyToManyField(through='projects.Application', to=settings.AUTH_USER_MODEL),
        ),
    ]