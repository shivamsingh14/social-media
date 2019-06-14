from django.conf.urls import url
from rest_framework.authtoken import views

from app.users.views import (
                   UserViewSet,
                   VerifyUser,
                   UserLogoutView,
                   UserDetailViewSet,
                   FriendsViewSet,
                   FriendRequest,
                   ResponseRequest,
                   PendingViewSet,
                   SentRequestViewSet,
                   MyProfilelViewSet,
                   ProfileViewSet)
# from app.posts.views import ProfileViewSet

urlpatterns = [
    url(r'^login/$', views.ObtainAuthToken.as_view(), name="login"),
    url(r'^logout/$', UserLogoutView.as_view(), name="logout"),
    url(r'^details/(?P<uid>[0-9]+)$', UserDetailViewSet.as_view(
        {
            'get': 'retrieve'
        }
        ), name="userDetail"),
    url(r'^profile/$', MyProfilelViewSet.as_view(
        {
            'get': 'retrieve'
        }
        ), name="profile"),
    url(r'^profile/(?P<uid>[0-9]+)$', ProfileViewSet.as_view(
        {
            'get': 'retrieve'
        }
        ), name="profile"),
    url(r'^friends/$', FriendsViewSet.as_view(
        {
            'get': 'list'
        }
        ), name="friends"),
    url(r'^$', UserViewSet.as_view(
        {
            'post': 'create',
            'get': 'list',
            'patch': 'partial_update'
        }
    ), name="users"),
    url(r'^friend-request/(?P<uid>[0-9]+)$', FriendRequest.as_view(), name="friendRequest"),
    url(r'^accept/$', ResponseRequest.as_view(
        {
            'post': 'create'
        }
    ), name="ResponseRequest"),
    url(r'^sent-request/(?P<uid>[0-9]+)/$', SentRequestViewSet.as_view(
        {
            'get': 'list',
            'delete': 'destroy'
        }
    ), name="SentRequest"),
    url(r'^pending/$', PendingViewSet.as_view(
        {
            'get': 'list'
        }
    ), name="ResponseRequest"),
    url(r'confirm/(?P<uid>[0-9]+)/(?P<token>[^$]+)/$', VerifyUser.as_view(),
        name="reset_password_confirm")
]
