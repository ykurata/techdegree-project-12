# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-25 19:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20181025_0436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='filled',
            new_name='position_filled',
        ),
    ]
