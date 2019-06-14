from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20190411_0953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='creation_time',
        ),
        migrations.AddField(
            model_name='post',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='post',
            name='password',
            field=models.CharField(default=datetime.datetime(2019, 4, 12, 10, 11, 18, 898135, tzinfo=utc), max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
