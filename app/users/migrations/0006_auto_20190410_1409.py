
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190410_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_status',
            field=models.BooleanField(default=False),
        ),
    ]
