# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-03 17:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0005_auto_20160703_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blognavigationitem',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
    ]