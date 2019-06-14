from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_post_updation_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='post',
            name='password',
        ),
    ]
