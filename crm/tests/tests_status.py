from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User


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

    def test_status_list(self):
        access_token = self.login_token(user=self.admin)
        uri = reverse('status-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)


    def test_create_status(self):
        pass

    def test_retrieve_status(self):
        pass

    def test_update_status(self):
        pass

    def test_delete_status(self):
        pass
