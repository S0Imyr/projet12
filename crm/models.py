from django.db import models
from django.conf import settings


class Client(models.Model):
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=250, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['last_name', 'email']

    def __str__(self):
        return "{self.last_name}: {self.company_name}"
    
    class Meta:
        ordering = ['-last_name']


class Contract(models.Model):
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    client = models.ForeignKey(to=Client, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    signed = models.BooleanField(default=False)
    amount = models.FloatField(blank=True, null=True)
    payment_due =  models.DateTimeField("Payment due date", blank=True, null=True)

    def __str__(self):
        return "Contract {self.id} - {client} ({sales_contact})"

    class Meta:
        ordering = ['-date_created']

class Status(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-title']
        verbose_name_plural = "statuses"


class Event(models.Model):
    title = models.CharField(max_length=50)
    client = models.ForeignKey(to=Client, on_delete=models.SET_NULL, blank=True, null=True)
    contract_id = models.OneToOneField(to=Contract, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    event_status = models.ForeignKey(to=Status, on_delete=models.SET_NULL, blank=True, null=True)  ### Default
    attendees = models.IntegerField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-title']
