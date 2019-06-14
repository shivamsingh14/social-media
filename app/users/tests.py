from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import TestCase

from django_dynamic_fixture import G
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient

from app.users.models import User
from app.posts.models import Post


class TestSignUpApi(APITestCase):

    def setUp(self):
        self.instance = G(User)
        self.instance.password = 'jtg12345'
        self.instance.save()

    def test_signup(self):
        self.data = {
            "first_name": self.instance.id,
            "email": "a1@dynamicfixture.com",
            "password": self.instance.password
            }
        url = reverse('user:users')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestLoginApi(APITestCase):

    def setUp(self):
        self.password = make_password('jtg12345')
        self.instance = G(User)
        self.instance.password = self.password
        self.instance.save()

    def test_login(self):
        url = reverse('user:login')
        self.data = {
            "username": self.instance.email,
            "password": 'jtg12345'
        }
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestLogoutApi(APITestCase):

    def setUp(self):
        self.user = G(User)

    def test_user_logout_request(self):
        url = reverse('user:logout')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestUserDetailApi(APITestCase):

    def setUp(self):
        self.instance = G(User)
        self.instance.password = 'jtg12345'
        self.instance.save()
        data = {
            "first_name": self.instance.id,
            "email": "a1@dynamicfixture.com",
            "password": self.instance.password
            }
        url = reverse('user:users')
        self.response = self.client.post(url, data)

    def test_user_detail(self):
        kwargs = {"uid": self.response.data['id']}
        url = reverse('user:userDetail', kwargs=kwargs)
        self.client = APIClient()
        self.client.force_authenticate(user=self.instance)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# class TestProfileListApi(APITestCase):

#     def setUp(self):
#         self.post = G(Post)
#         self.user = G(User)

#     def test_profile_list(self):
#         kwargs = {"uid": self.post.owner}
#         url = reverse('user:profile', kwargs=kwargs)
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserListApi(APITestCase):

    def setUp(self):
        self.user = G(User)

    def test_user_list(self):
        url = reverse('user:users')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserUpdateApi(APITestCase):

    def setUp(self):
        self.user = G(User)

    def test_user_update(self):
        url = reverse('user:users')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": self.user.first_name
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)