from django.db import models

from client.models import Client
from dealer.models import Dealer
from restaurant.models import Item


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=12)


class Delivery(models.Model):
    """ restaurant """
    id = models.AutoField(primary_key=True)
    rank = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=None, related_name='delivery')
    dealer = models.ForeignKey(Dealer, on_delete=None, related_name='deliveries')
    client = models.ForeignKey(Client, on_delete=None, related_name='deliveries')
    status = models.ForeignKey(Status, on_delete=None, related_name='deliveries')
