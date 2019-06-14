from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20190412_1011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='updation_time',
        ),
    ]
