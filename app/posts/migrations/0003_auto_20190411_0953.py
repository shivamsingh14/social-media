from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_auto_20190410_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='creation_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='updation_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.IntegerField(choices=[(0, 'Private'), (1, 'Added Users'), (2, 'Following'), (3, 'Public')]),
        ),
        migrations.AlterUniqueTogether(
            name='visibilityuserpost',
            unique_together=set([('post', 'user')]),
        ),
    ]
