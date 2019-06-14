
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190410_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendstatus',
            name='following_status',
            field=models.IntegerField(choices=[(0, 'First user follows second'), (1, 'Second user follows first'), (2, 'Both follow each other'), (3, 'None follow each other')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendstatus',
            unique_together=set([('user_1', 'user_2')]),
        ),
    ]
