
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20190416_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_from', to=settings.AUTH_USER_MODEL)),
                ('request_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
