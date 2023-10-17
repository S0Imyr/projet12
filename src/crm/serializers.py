from rest_framework import serializers
from .models import Client, Contract, Event, Status


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'date_created', 'date_updated', 'sales_contact', 'active']
        read_only_fields = ['id']


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['sales_contact', 'client', 'date_created', 'date_updated', 'signed', 'amount', 'payment_due']
        read_only_fields = ['id']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'contract', 'title', 'client', 'date_created', 'date_updated', 'support_contact', 'event_status', 'attendees', 'event_date', 'notes']
        read_only_fields = ['id']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'title', 'description']
        read_only_fields = ['id']  
        