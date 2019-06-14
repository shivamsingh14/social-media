import datetime
import pytz

from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

from app.commons.constants import MAX_LENGTH_DICT


class CommonModelMixin(object):
    """
    Common model to store creation and updation time of posts
    """

    creation_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    updation_time = models.DateTimeField(auto_now=False, auto_now_add=False)


class SoftDeletionManager(models.Manager):
    """
    Manager to return objects excluding soft deleted objects
    """

    def get_queryset(self):
        return SoftDeletionQuerySet(self.model).filter(deleted_at=None)


class AllObjectsManager(models.Manager):
    """
    Manager to return all the objects
    """
    def get_queryset(self):
        return super(AllObjectsManager, self).get_queryset().all()


class SoftDeletionModel(models.Model):
    """
    Model to implement soft delete functionality
    """
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()


class SoftDeletionQuerySet(QuerySet):
    """
    Soft Deletion queryset
    """
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())
