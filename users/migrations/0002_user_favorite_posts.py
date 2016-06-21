# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-20 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_posts',
            field=models.ManyToManyField(blank=True, to='blog.Post'),
        ),
    ]
