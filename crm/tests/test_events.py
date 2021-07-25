from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User, Group

from datetime import datetime, timezone

from crm.models import Client, Contract, Status, Event


class EventTests(APITestCase):
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        print(Status.objects)
        cls.groups = [Group.objects.create(name='Support'), Group.objects.create(name='Sales'), Group.objects.create(name='Management'), Group.objects.create(name='Guest')]
        cls.support_users = [
            User.objects.create_user(username="Support1", email="support1@test.com",
            password="teamsupport1", first_name="User1", last_name="Support"),
            User.objects.create_user(username="Support2", email="support2@test.com",
            password="teamsupport2", first_name="User2", last_name="Support")
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
                amount=40000, payment_due=datetime(2022, 5, 21, 20, 8, 7, 127325, tzinfo=timezone.utc)
            ),
            Contract.objects.create(
                sales_contact=cls.salers[0], client=cls.clients[0], signed=True,
                amount=80000, payment_due=datetime(2021, 5, 21, 20, 8, 7, 127325, tzinfo=timezone.utc)
            ),
            Contract.objects.create(
                sales_contact=cls.salers[1], client=cls.clients[0], signed=True,
                amount=50000, payment_due=datetime(2021, 7, 5, 20, 8, 7, 127325, tzinfo=timezone.utc)
            ),
        ]

        cls.statuses = [
            Status.objects.create(title="Coming", description="The event is comming"),
            Status.objects.create(title="In progress", description="The event is in progress"),
            Status.objects.create(title="Over", description="The event is finished")
        ]

        cls.events = [
            Event.objects.create(
                title='Event1', contract_id=cls.contracts[0].id, client=cls.clients[0],
                support_contact=cls.support_users[0], event_status=cls.statuses[0]),
            Event.objects.create(
                title='Event2', contract_id=cls.contracts[2].id, client=cls.clients[0],
                support_contact=cls.support_users[0], event_status=cls.statuses[2]),
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

    def test_event_list_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('event-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_event_list_as_saler(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('event-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_event_list_as_support(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('event-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_event_list_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('event-list')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_create_event_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('event-list')
        post_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

    def test_create_event_as_saler(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('event-list')
        post_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

    def test_create_event_as_support(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('event-list')
        post_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_create_event_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('event-list')
        post_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_retrieve_event_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_retrieve_event_as_saler_not_contact(self):
        access_token = self.login_token(user=self.salers[1])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_retrieve_event_as_saler_contact(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_retrieve_event_list_as_support_not_contact(self):
        access_token = self.login_token(user=self.support_users[1])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_retrieve_event_list_as_support_contact(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_retrieve_event_list_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_update_event_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        put_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_update_event_as_saler_not_contact(self):
        access_token = self.login_token(user=self.salers[1])
        uri = reverse('event-detail', args=[self.events[0].id])
        put_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_update_event_as_saler_contact(self):
        access_token = self.login_token(user=self.salers[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        put_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_update_event_as_support_not_contact(self):
        access_token = self.login_token(user=self.support_users[1])
        uri = reverse('event-detail', args=[self.events[0].id])
        put_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_update_event_as_support_contact(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        put_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    # def test_update_event_as_support_contact_but_finished(self):
    #     access_token = self.login_token(user=self.support_users[0])
    #     uri = reverse('event-detail', args=[self.events[1].id])
    #     put_data = dict(
    #         contract=self.contracts[1].id, title='EventTestTitle',
    #         client=self.clients[0].id, support_contact=self.support_users[0].id, 
    #         event_status=self.statuses[2].id, attendees=5000,
    #         event_date=datetime(year=2021, month=5, day=21), notes="")
    #     response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_update_event_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        put_data = dict(
            contract=self.contracts[1].id, title='EventTestTitle',
            client=self.clients[0].id, support_contact=self.support_users[0].id, 
            event_status=self.statuses[2].id, attendees=5000,
            event_date=datetime(year=2022, month=5, day=21), notes="")
        response = self.client.put(uri, data=put_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)


    def test_delete_event_as_manager(self):
        access_token = self.login_token(user=self.management_users[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.delete(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

    def test_delete_event_as_saler(self):
        access_token = self.login_token(user=self.salers[1])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.delete(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_delete_event_list_as_support(self):
        access_token = self.login_token(user=self.support_users[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.delete(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_delete_event_list_as_guest(self):
        access_token = self.login_token(user=self.guests[0])
        uri = reverse('event-detail', args=[self.events[0].id])
        response = self.client.delete(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
