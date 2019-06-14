from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from app.users.models import User, FriendStatus, PendingRequests
from app.users.serializers import(
                        UserSerializer,
                        UserDetailSerializer,
                        FriendsSerializer,
                        ResponseRequestSerializer,
                        FriendRequestSerializer,
                        UserListSerializer,
                        UpdateProfileSerializer,
                        PendingSerializer,
                        SentSerializer,
                        MyProfileSerializer)
from app.users.tasks import send_friend_request_task, user_verification_task
from app.commons.permissions import ViewUserDetailsPermission


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = {
            'first_name': ['icontains']
        }


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    """
    Handles create operation on User
    """
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserFilter
    queryset = User.objects.all()

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(UserViewSet, self).get_permissions()

    serializer_classes = {
        'create': UserSerializer,
        'list': UserListSerializer,
        'partial_update': UpdateProfileSerializer
    }

    def perform_create(self, serializer):
        serializer.save()
        user = serializer.instance
        user_email = user.email
        url = "{}confirm/{}/{}".format(
            settings.BASE_URL,
            user.id,
            user.user_token
            )
        user_verification_task.delay(url, user_email)

    def get_serializer_class(self):
        return self.serializer_classes[self.action]


class VerifyUser(APIView):
    """
    ViewSet to verify the signed up user based on link received through mail
    """
    permission_classes = ()

    def get(self, request, *args, **kwargs):

        token = kwargs.get('token')
        uid = kwargs.get('uid')
        user = User.objects.get(id=uid)
        if token == user.user_token:
            user.verification_status = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserLogoutView(APIView):
    """
    Handels the Logout Operation on User
    """

    def delete(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Viewset for displaying the details of the user
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserDetailSerializer

    def get_object(self):
        if self.kwargs['uid'] == '0':
            return User.objects.get(id=self.request.user.id)
        else:
            return User.objects.get(id=self.kwargs['uid'])


class FriendsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset to display user's friends
    """

    def get_queryset(self):
        return FriendStatus.objects.filter(user_1=self.request.user).select_related('user_2')
    serializer_class = FriendsSerializer


class FriendRequest(APIView):
    """
    Handles friend requests operation
    """

    def post(self, request, *args, **kwargs):
        recipient_email = User.objects.get(id=kwargs['uid']).email
        sending_email = self.request.user.email
        user_name = self.request.user.first_name
        request.data['request_from'] = self.request.user.id
        request.data['request_to'] = kwargs['uid']
        serializer = FriendRequestSerializer(data=request.data)
        url = "{}{}". format(
            settings.BASE_URL,
            'pending',
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_friend_request_task.delay(url, sending_email, recipient_email, user_name)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResponseRequest(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Viewset to update friend's status of two users according to response of the user
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = ResponseRequestSerializer


class PendingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet to display list of all the pending requests
    """
    def get_queryset(self):
        return PendingRequests.objects.filter(request_to=self.request.user).select_related('request_from')

    permission_classes = (IsAuthenticated, )
    serializer_class = PendingSerializer


class SentRequestViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    ViewSet to display list of sent requests by users and cancel any sent request
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = SentSerializer

    def get_queryset(self):
        return PendingRequests.objects.filter(request_from=self.request.user).select_related('request_to')

    def get_object(self):
        return PendingRequests.all_objects.get(request_to=self.kwargs['uid'], request_from=self.request.user)


class MyProfilelViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = MyProfileSerializer

    def get_object(self):
        return self.request.user


class ProfileViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserDetailSerializer

    def get_object(self):
        return User.objects.get(id=self.kwargs['uid'])
