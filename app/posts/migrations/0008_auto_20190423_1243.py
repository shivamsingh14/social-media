# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-23 12:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_post_content_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VisibilityUserPost',
            new_name='PostVisibility',
        ),
    ]
