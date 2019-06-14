
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20190416_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendstatus',
            name='following_status',
            field=models.IntegerField(choices=[(0, 'First user follows second'), (1, 'Both follow each other')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
    ]
