# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 11:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20160326_1149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='linkes',
            new_name='likes',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='linkes',
            new_name='likes',
        ),
    ]
