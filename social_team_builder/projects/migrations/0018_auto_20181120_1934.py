# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_remove_position_applicants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
