from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

from dealer.models import Dealer, DealerSerializer
from restaurant.models import Restaurant, Item, RestaurantSerializer, ItemSerializer, UserSerializer


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=None, primary_key=True)
    latitude = models.DecimalField(decimal_places=120, max_digits=128, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=120, max_digits=128, null=True, blank=True)

    '''to format the object'''
    def __str__(self):
        return '{} <{}>'.format(self.user.first_name, self.user.id)

    class Meta:
        db_table = 'client'


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Client
        fields = ['user_id', 'latitude', 'longitude', 'user']


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=None)
    client = models.ForeignKey(Client, on_delete=None)
    # dealer = models.ForeignKey(Dealer, on_delete=None)
    item = models.ForeignKey(Item, on_delete=None)
    status = models.IntegerField(default=1)


class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    restaurant = RestaurantSerializer()
    dealer = DealerSerializer()
    item = ItemSerializer()

    class Meta:
        model = Order
        fields = ('id', 'client', 'dealer', 'restaurant','item')
