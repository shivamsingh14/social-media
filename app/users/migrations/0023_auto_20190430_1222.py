# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-30 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20190430_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_token',
            field=models.CharField(max_length=64),
        ),
    ]