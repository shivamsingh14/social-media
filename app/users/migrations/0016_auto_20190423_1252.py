# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-23 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_delete_testsoftdelete'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendstatus',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]