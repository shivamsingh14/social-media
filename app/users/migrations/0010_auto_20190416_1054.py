
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_testsoftdelete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendstatus',
            name='following_status',
            field=models.IntegerField(choices=[(0, 'First user follows second'), (1, 'Second user follows first'), (2, 'Both follow each other')]),
        ),
        migrations.AlterField(
            model_name='testsoftdelete',
            name='name',
            field=models.CharField(max_length=2058),
        ),
    ]
