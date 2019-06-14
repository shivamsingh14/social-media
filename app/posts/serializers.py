from rest_framework import serializers

from app.posts.models import Post
from app.users.models import User


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for creation of post
    """
    class Meta(object):
        model = Post
        fields = ('id', 'content_text', 'content_image', 'visibility')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(PostSerializer, self).create(validated_data)


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('first_name', 'last_name', 'gender', 'email')


class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer to display list of posts along owner's details of every post
    """

    owner = UserInfoSerializer()

    class Meta(object):
        model = Post
        fields = ('id', 'visibility', 'owner', 'content_text', 'content_image')