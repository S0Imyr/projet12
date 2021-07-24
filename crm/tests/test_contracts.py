from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User, Group

import datetime

from crm.models import Client, Contract


class ContractTests(APITestCase):
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
                sales_contact=cls.salers[0], client=cls.clients[0], signed=True,
                amount=80000, payment_due=datetime(year=2021, month=5, day=21)
            ),
            Contract.objects.create(
                sales_contact=cls.salers[0], client=cls.clients[1], signed=False,
                amount=40000, payment_due=datetime(year=2022, month=5, day=21)
            ),
        ]

    @classmethod
    def tearDownClass(cls):
        cls.admin = None
        User.objects.all().delete()

    def login_token(self, user):
        self.client.force_login(user=user)
        tokens = RefreshToken.for_user(user)
        access_token = str(tokens.access_token)
        return access_token
    
    def test_contract_list(self):
        access_token = self.login_token(user=self.admin)
        uri = reverse('contract-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)


    def test_create_contract(self):
        pass

    def test_retrieve_contract(self):
        pass

    def test_update_contract(self):
        pass

    def test_delete_contract(self):
        pass
