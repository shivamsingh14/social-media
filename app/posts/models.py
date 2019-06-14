from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models

from app.commons.constants import MAX_LENGTH_DICT
from app.commons.modelMixins import CommonModelMixin, SoftDeletionModel


class Post(CommonModelMixin, SoftDeletionModel):

    """
    model to store every post's attributes
    """

    PRIVATE = 0
    ADDED_USERS = 1
    FOLLOWING = 2
    PUBLIC = 3

    VISIBILITY_CHOICES = (
        (PRIVATE, 'Private'),
        (ADDED_USERS, 'Added Users'),
        (FOLLOWING, 'Following'),
        (PUBLIC, 'Public')
    )

    content_text = models.CharField(max_length=MAX_LENGTH_DICT["long"])
    content_image = models.ImageField(upload_to='post', null=True, blank=True)
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userPosts')
    post_visibility = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PostVisibility')

    def __unicode__(self):
        return '{}'.format(self.content_text)


class PostVisibility(SoftDeletionModel):

    """
    model to set visibilty of posts to certain users
    """

    post = models.ForeignKey(Post, related_name='users')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')

    class Meta:
        unique_together = ('post', 'user',)
