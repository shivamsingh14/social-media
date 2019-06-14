from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from app.commons.constants import MAX_LENGTH_DICT
from app.commons.modelMixins import CommonModelMixin, SoftDeletionModel


class MyUserManager(BaseUserManager):

    def create_user(self, first_name, email, password):
        """
        A function to add a new user to the database
        """
        if not email:
            raise ValueError('User must have a email address')
        elif not first_name:
            raise ValueError('User must have a first name')
        elif not password:
            raise ValueError('User must have a password')
        user = User(first_name=first_name, email=email)
        user.set_password(password)
        return user

    def create_superuser(self, email, password, first_name):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name
        )
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class User(CommonModelMixin, AbstractBaseUser, SoftDeletionModel):

    """
    User Model that stores user's attributes
    """

    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )

    first_name = models.CharField(max_length=MAX_LENGTH_DICT["title"])
    last_name = models.CharField(max_length=MAX_LENGTH_DICT["title"], blank=True, null=True)
    username = models.CharField(max_length=MAX_LENGTH_DICT["title"], blank=True, null=True)
    email = models.EmailField(max_length=MAX_LENGTH_DICT["email"], unique=True)
    is_staff = models.BooleanField(default=False)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, null=True, default='M')
    profile_picture = models.ImageField(upload_to='post', null=True, blank=True)
    user_token = models.CharField(max_length=MAX_LENGTH_DICT["title"])
    verification_status = models.BooleanField(default=False)
    user_friends = models.ManyToManyField('self', through='FriendStatus', symmetrical=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def save(self, *args, **kwargs):
        self.user_token = uuid.uuid1()
        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app"
        return True

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return '{}.{}'.format(self.id, self.first_name)


class FriendStatus(SoftDeletionModel):

    """
    Model class for friend status of a user with other users
    """

    USER1_FOLLOWS_USER2 = 0
    BOTH_FOLLOW = 1

    FOLLOWING_CHOICES = (
        (USER1_FOLLOWS_USER2, 'First user follows second'),
        (BOTH_FOLLOW, 'Both follow each other')
    )

    user_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend')
    user_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user2')
    following_status = models.IntegerField(choices=FOLLOWING_CHOICES, default=0)

    def clean(self):
        if FriendStatus.objects.filter(user_2=self.user_1, user_1=self.user_2).exists():
            raise ValidationError('This user cannot create request')

    class Meta:
        unique_together = ('user_1', 'user_2',)


class PendingRequests(SoftDeletionModel):
    """
    Model class for pending requests to a user
    """
    request_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='request_from')
    request_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='request_to')

    class Meta:
        unique_together = ('request_from', 'request_to',)
