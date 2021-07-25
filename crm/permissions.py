from django.test import client
from rest_framework.permissions import BasePermission, SAFE_METHODS

from crm.models import Contract, Event

class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Management").exists():
            return True
        elif request.user.groups.filter(name="Sales").exists() or request.user.groups.filter(name="Support").exists():
            if request.method == 'POST':
                return request.user.groups.filter(name="Sales").exists()
            elif request.method == 'PUT' or request.method == 'GET':
                return True
            else:
                return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Management").exists():
            return True
        elif request.user.groups.filter(name="Sales").exists():
            if request.method == 'PUT' or request.method == 'GET':
                if request.user == obj.sales_contact:
                    return True
                else:
                    contracts = Contract.objects.filter(client=obj)
                    sales_contacts = []
                    for contract in contracts:
                        sales_contacts.append(contract.sales_contact)
                    print('Sales contact', sales_contacts)
                    return request.user in sales_contacts
            else:
                return False
        elif request.user.groups.filter(name="Support").exists():
            if request.method == 'GET':
                events = Event.objects.filter(client=obj)
                support_contacts = []
                for event in events:
                    support_contacts.append(event.support_contact)
                print('Support contact', support_contacts)
                return request.user in support_contacts
            else:
                return False
        else:
            return False


class ContractPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Guest").exists():
            return False
        else:
            if request.method in SAFE_METHODS:
                return True
            elif request.method == 'POST' or request.method == 'PUT':
                if request.user.groups.filter(name="Management").exists() or \
                request.user.groups.filter(name="Sales").exists():
                    return True
                else:
                    return False
            else:
                return request.user.groups.filter(name="Management").exists()

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Management").exists():
            return True
        elif request.user.groups.filter(name="Sales").exists():
            if request.method in SAFE_METHODS:
                return True
            elif request.method == 'PUT':
                return request.user == obj.sales_contact
            else:
                return False
        elif request.user.groups.filter(name="Support").exists():
            return request.method in SAFE_METHODS
        else:
            return False

class EventPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Management").exists():
            return True
        elif request.user.groups.filter(name="Sales").exists() or request.user.groups.filter(name="Support").exists():
            if request.method == 'POST':
                return request.user.groups.filter(name="Sales").exists()
            elif request.method == 'PUT' or request.method == 'GET':
                return True
            else:
                return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Management").exists():
            return True
        elif request.user.groups.filter(name="Sales").exists():
            if request.method == 'PUT' or request.method == 'GET':
                if request.user == obj.client.sales_contact:
                    return True
                else:
                    return False
            else:
                return False
        elif request.user.groups.filter(name="Support").exists():
            if request.method == 'PUT' or request.method == 'GET':
                if request.user == obj.support_contact:
                    return not obj.event_status.id == 3
                else:
                    return False
            else:
                return False
        else:
            return False


class StatusPermission(BasePermission):
    message = 'Restricted to management team'
    
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Management').exists():
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Management').exists():
            return True
        else:
            return False
