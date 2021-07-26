from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User, Group

from datetime import date, timezone

from crm.models import Client, Contract, Event, Status


class StatusTests(APITestCase):
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
            password="teamsales1", first_name="User1", last_name="Sales"),
            User.objects.create_user(username="Saler2", email="saler2@test.com",
            password="teamsales2", first_name="User2", last_name="Sales")
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
            password="teamguests1", first_name="User1", last_name="Guest"),
            User.objects.create_user(username="Guest2", email="guest2@test.com",
            password="teamguests2", first_name="User2", last_name="Guest")
            ]
        for guest in cls.guests:
            guest.groups.set([cls.groups[3]])

        cls.clients = [
            Client.objects.create(
            first_name="Active", last_name="client1", email="client1@test.com",
            phone=12, mobile=12, company_name='CompanyCorp1', sales_contact=cls.salers[0],
            active=True),
            Client.objects.create(
            first_name="Unactive", last_name="client2", email="client2@test.com",
            phone=12, mobile=12, company_name='CompanyCorp2',
            active=False),
            ]

        cls.contracts = [
            Contract.objects.create(
                sales_contact=cls.salers[0], client=cls.clients[1], signed=False,
                amount=40000, payment_due=date(2022, 5, 21)
            ),
            Contract.objects.create(
                sales_contact=cls.salers[0], client=cls.clients[0], signed=True,
                amount=80000, payment_due=date(2021, 5, 21)
            ),
            Contract.objects.create(
                sales_contact=cls.salers[1], client=cls.clients[0], signed=True,
                amount=50000, payment_due=date(2021, 7, 5)
            ),
        ]

        cls.statuses = [
            Status.objects.create(title="Coming", description="The event is comming"),
            Status.objects.create(title="In progress", description="The event is in progress"),
            Status.objects.create(title="Over", description="The event is finished")
        ]

    @classmethod
    def tearDownClass(cls):
        Group.objects.all().delete()
        User.objects.all().delete()
        Client.objects.all().delete()
        Contract.objects.all().delete()
        Status.objects.all().delete()
        Event.objects.all().delete()

    def login_token(self, user):
        self.client.force_login(user=user)
        tokens = RefreshToken.for_user(user)
        access_token = str(tokens.access_token)
        return access_token

    def test_status_list_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('status-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_status_list_as_saler(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('status-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_status_list_as_support(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('status-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_status_list_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('status-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_status_list_unauthenticated(self):
        uri = reverse('status-list')
        response = self.client.get(uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_create_status_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('status-list')
        post_data = dict(title="TestStatus", description="Status test")
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

    def test_create_status_as_saler(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('status-list')
        post_data = dict(title="TestStatus", description="Status test")
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')

    def test_create_status_as_support(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('status-list')
        post_data = dict(title="TestStatus", description="Status test")
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')

    def test_create_status_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('status-list')
        post_data = dict(title="TestStatus", description="Status test")
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')

    def test_retrieve_status_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_retrieve_status_as_saler(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')

    def test_retrieve_status_as_support(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')

    def test_retrieve_status_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')

    def test_update_status_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        put_data = dict(title="TestStatus", description="Status test")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_update_status_as_saler(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        put_data = dict(title="TestStatus", description="Status test")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')

    def test_update_status_as_support(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        put_data = dict(title="TestStatus", description="Status test")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')

    def test_update_status_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        put_data = dict(title="TestStatus", description="Status test")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')

    def test_delete_status_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        response = self.client.delete(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

    def test_delete_status_as_saler(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        response = self.client.delete(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')


    def test_delete_status_as_support(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        response = self.client.delete(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')


    def test_delete_status_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('status-detail', args=[self.statuses[1].id])
        response = self.client.delete(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        self.assertEqual(response.content, b'{"detail":"Restricted to management team"}')
