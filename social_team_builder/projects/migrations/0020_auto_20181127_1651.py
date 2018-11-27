# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-27 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_position_applicants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Description...'),
        ),
        migrations.AlterField(
            model_name='position',
            name='position_filled',
            field=models.BooleanField(default=False, verbose_name='Position filled'),
        ),
        migrations.AlterField(
            model_name='position',
            name='skill',
            field=models.CharField(choices=[('Android', 'Android Developer'), ('Design', 'Designer'), ('Java', 'Java Developer'), ('PHP', 'PHP Developer'), ('Python', 'Python Developer'), ('Rails', 'Rails Developer'), ('Wordpress', 'Wordpress Developer'), ('iOS', 'iOS Developer')], default='', max_length=20, verbose_name='Related skills'),
        ),
        migrations.AlterField(
            model_name='position',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
    ]
