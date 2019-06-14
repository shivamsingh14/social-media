from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Q

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from app.posts.serializers import PostSerializer, PostListSerializer
from app.users.serializers import UserDetailSerializer, FriendsSerializer
from app.posts.models import Post
from app.users.models import User, FriendStatus


class PostViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Handles creation and list operation on Post
    """

    pagination_class = None

    def get_queryset(self):
        if self.action == 'list':
            following = FriendStatus.objects.filter(user_1=self.request.user).values_list('user_2', flat=True)
            mutual_followers = FriendStatus.objects.filter(user_2=self.request.user, following_status=Post.ADDED_USERS).values_list('user_1', flat=True)
            queryset = Post.objects.filter(
                Q(visibility=Post.PUBLIC) |
                Q(
                    Q(visibility=Post.FOLLOWING) &
                    Q(owner_id__in=following) |
                    Q(owner_id__in=mutual_followers)
                ) |
                Q(visibility=Post.ADDED_USERS, users__user=self.request.user)
            ).select_related('owner')
        else:
            queryset = Post.objects.all()
        return queryset

    serializer_classes = {
        'create': PostSerializer,
        'list': PostListSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes[self.action]
