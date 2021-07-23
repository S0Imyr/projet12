from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User, Group


class UserTests(APITestCase):
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        cls.groups = [Group.objects.create(name='Support'), Group.objects.create(name='Sales'), Group.objects.create(name='Management'), Group.objects.create(name='Guest')]
        cls.support_users = [
            User.objects.create_user(username="Support1", email="support1@test.com",
            password="teamsupport1", first_name="User1", last_name="Support")
            ]
        for support_user in cls.support_users:
            support_user.groups.set([cls.groups[0]])
        cls.salers = [
            User.objects.create_user(username="Saler1", email="saler1@test.com",
            password="teamsales1", first_name="User1", last_name="Sales")
            ]
        for saler in cls.salers:
            saler.groups.set([cls.groups[1]])
        cls.management_users = [
            User.objects.create_user(username="Manager1", email="manager1@test.com",
            password="teammanagement1", first_name="User1", last_name="Management")
            ]
        for management_user in cls.management_users:
            management_user.groups.set([cls.groups[2]])
        cls.guests = [
            User.objects.create_user(username="Guest1", email="guest1@test.com",
            password="teamguests1", first_name="User1", last_name="Guest")
            ]
        for guest in cls.guests:
            guest.groups.set([cls.groups[3]])

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def login_token(self, user):
        self.client.force_login(user=user)
        tokens = RefreshToken.for_user(user)
        access_token = str(tokens.access_token)
        return access_token
    
    def test_user_list(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('user-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_user_list_unauthenticated(self):
        uri = reverse('user-list')
        response = self.client.get(uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_create_user_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('user-list')
        post_data = dict(
            username="username", email="email@test.com",
            first_name="first_name", last_name="last_name",
            group=self.groups[0])
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

    def test_create_user_as_saler(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('user-list')
        post_data = dict(
            username="username", email="email@test.com",
            first_name="first_name", last_name="last_name",
            group=self.groups[0])
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_create_user_as_support(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('user-list')
        post_data = dict(
            username="username", email="email@test.com",
            first_name="first_name", last_name="last_name",
            group=self.groups[0])
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_create_user_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('user-list')
        post_data = dict(
            username="username", email="email@test.com",
            first_name="first_name", last_name="last_name",
            group=self.groups[0])
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        print(response.content)

    def test_retrieve_user(self):
        pass

    def test_update_user(self):
        pass

    def test_delete_user(self):
        pass
