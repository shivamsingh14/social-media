from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.password_validation import validate_password

from rest_framework.authtoken.models import Token
from rest_framework import serializers

from app.users.models import User, FriendStatus, PendingRequests
from app.posts.models import Post


class UserSerializer(serializers.ModelSerializer):

    """
    User model Signup Serializer
    """
    token = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'passsword'})

    class Meta(object):
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'email', 'token', 'password')

    def validate(self, data):
        if self.instance:
            return super(UserSerializer, self).validate(data)
        else:
            user = User(first_name=data['first_name'],
                        email=data['email'])
            validate_password(data['password'], user)
            data['password'] = make_password(data['password'])
            return data

    def create(self, validated_data):

        """
        overriding default create to insert token
        """
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        token = Token.objects.create(user=instance)
        instance.token = token
        return instance


class PostList(serializers.ModelSerializer):

    class Meta(object):
        model = Post
        fields = ('id', )


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for details of the user
    """
    userPost = serializers.SerializerMethodField()

    class Meta(object):
        model = User

        fields = ('id', 'first_name', 'last_name', 'gender', 'email', 'verification_status', 'userPost')

    def get_userPost(self, obj):
        return PostList(Post.objects.filter(owner=obj, visibility=3), many=True).data


class MyProfileSerializer(serializers.ModelSerializer):
    userPost = serializers.SerializerMethodField()

    class Meta(object):
        model = User

        fields = ('id', 'first_name', 'last_name', 'gender', 'email', 'verification_status', 'userPost')

    def get_userPost(self, obj):
        return PostList(Post.objects.filter(owner=obj), many=True).data


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    serializer to update the details of the user
    """

    class Meta(object):
        model = User
        fields = ('first_name', )


class FriendsSerializer(serializers.ModelSerializer):
    """
    Serializer to list friends of the user
    """

    user_2 = UserDetailSerializer()

    class Meta(object):
        model = FriendStatus
        fields = ('user_2', )
        read_only_fields = ('user_2', )


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer to display the list of the users
    """
    class Meta(object):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer to handle follow request of one user to another
    """

    class Meta(object):
        model = PendingRequests
        fields = ('request_from', 'request_to', )

    def validate(self, data):
        if FriendStatus.objects.filter(user_1=data['request_from'], user_2=data['request_to']):
            raise ValidationError('User already Follows')
        return data


class ResponseRequestSerializer(serializers.ModelSerializer):
    """
    Serializer to handle response of the user to the follow request
    """

    class Meta(object):
        model = FriendStatus
        fields = ('user_1', 'user_2', 'following_status', )

    def validate(self, data):
        if data['user_2'] != self.context['request'].user:
            raise ValidationError('Invalid user')

        requested_user = PendingRequests.objects.filter(request_to=self.context['request'].user).values_list('request_from', flat=True)
        if data['user_1'].id not in requested_user:
            raise ValidationError('No such user with follow request found')
        return data

    @transaction.atomic
    def create(self, validated_data):
        pending_instance = PendingRequests.objects.filter(request_from=self.context['request'].data['user_1'], request_to=self.context['request'].data['user_2'])
        if pending_instance.exists():
            pending_instance.delete()
        try:
            friend_instance = FriendStatus.objects.get(user_2=self.context['request'].data['user_1'], user_1=self.context['request'].data['user_2'])
            friend_instance.following_status = 1
            friend_instance.save()
            return friend_instance
        except FriendStatus.DoesNotExist:
            return super(ResponseRequestSerializer, self).create(validated_data)


class PendingSerializer(serializers.ModelSerializer):
    """
    Serializer to list the pending requests of users
    """
    request_from = UserDetailSerializer()

    class Meta(object):
        model = PendingRequests
        fields = ('request_from', 'request_to', )
        read_only_fields = ('request_from', 'request_to', )


class SentSerializer(serializers.ModelSerializer):

    request_to = UserDetailSerializer()

    class Meta(object):
        model = PendingRequests
        fields = ('request_from', 'request_to', )
        read_only_fields = ('request_from', 'request_to', )
