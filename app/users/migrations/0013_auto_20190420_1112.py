
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_pendingrequests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendstatus',
            name='following_status',
            field=models.IntegerField(choices=[(0, 'First user follows second'), (1, 'Both follow each other')], default=0),
        ),
        migrations.AlterUniqueTogether(
            name='pendingrequests',
            unique_together=set([('request_from', 'request_to')]),
        ),
    ]
