from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_text', models.CharField(max_length=2058)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('updation_time', models.DateTimeField(auto_now=True)),
                ('visibility', models.IntegerField(choices=[(0, 'Private'), (1, 'addedUsers'), (2, 'Following'), (3, 'Public')])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
