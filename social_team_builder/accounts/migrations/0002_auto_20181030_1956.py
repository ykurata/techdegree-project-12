# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-30 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='avator',
            new_name='image',
        ),
        migrations.AddField(
            model_name='user',
            name='skill',
            field=models.CharField(choices=[('Android', 'Android Developer'), ('Design', 'Designer'), ('Java', 'Java Developer'), ('PHP', 'PHP Developer'), ('Python', 'Python Developer'), ('Rails', 'Rails Developer'), ('Wordpress', 'Wordpress Developer'), ('iOS', 'iOS Developer')], default='', max_length=25),
        ),
    ]
