# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-26 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_remove_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='post'),
        ),
    ]