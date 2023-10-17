from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User


class UserTests(APITestCase):
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

    def test_group_list(self):
        pass

    def test_create_group(self):
        pass

    def test_retrieve_group(self):
        pass

    def test_update_group(self):
        pass

    def test_delete_group(self):
        pass