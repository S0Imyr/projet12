from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User


class AuthTests(APITestCase):
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        """Admin"""
        cls.admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')

    @classmethod
    def tearDownClass(cls):
        cls.admin = None
        User.objects.all().delete()

    def login_token(self, user):
        self.client.force_login(user=user)
        tokens = RefreshToken.for_user(user)
        access_token = str(tokens.access_token)
        return access_token

    def test_register(self):
        uri = reverse('register')
        post_data = dict(
            username="username", email="email@test.com",
            first_name="first_name", last_name="last_name", password="password")
        response = self.client.post(uri, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
