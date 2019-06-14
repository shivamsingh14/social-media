from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190410_0335'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following_status', models.IntegerField(choices=[(0, '1 follows 2'), (1, '2 follows 1'), (2, 'both follow'), (3, 'none follow')])),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_friends',
        ),
        migrations.AddField(
            model_name='friendstatus',
            name='user_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendstatus',
            name='user_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='user_friends',
            field=models.ManyToManyField(through='users.FriendStatus', to=settings.AUTH_USER_MODEL),
        ),
    ]
