
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20190420_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingrequests',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
