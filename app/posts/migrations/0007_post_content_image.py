from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20190412_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_image',
            field=models.ImageField(blank=True, null=True, upload_to='post'),
        ),
    ]
