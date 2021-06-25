from django.shortcuts import render
from rest_framework import viewsets

from .serializers import ClientSerializer, ContractSerializer, EventSerializer, StatusSerializer
from .models import Client, Contract, Event, Status


class ClientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Client instances.
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ContractViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Contract instances.
    """
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Event instances.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class StatusViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Status instances.
    """
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
