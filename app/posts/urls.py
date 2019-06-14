from django.conf.urls import url

from app.posts.views import PostViewSet

urlpatterns = [
    url(r'^$', PostViewSet.as_view(
        {
            'post': 'create',
            'get': 'list'
        }
    ), name="posts")
]
