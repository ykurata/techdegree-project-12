# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-13 14:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='notification',
            new_name='message',
        ),
    ]
