from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from client.models import Order, OrderSerializer
from restaurant.models import UserSerializer


class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=None, primary_key=True)
    latitude = models.DecimalField(decimal_places=120, max_digits=128)
    longitude = models.DecimalField(decimal_places=120, max_digits=128)
    status = models.IntegerField()

    def __str__(self):
        return '{} <{}>'.format(self.user.first_name, self.user.id)

    class Meta:
        db_table = 'dealer'


class DealerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Dealer
        fields = ['user_id', 'latitude', 'longitude', 'user','status']


"""
class Solicitude(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=None)
    dealer = models.ForeignKey(Dealer, on_delete=None)
    time = models.DecimalField(decimal_places=120, max_digits=128)


class SolicitudeSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    dealer = DealerSerializer()

    class Meta:
        model = Solicitude
        fields = ('id', 'order', 'dealer','time')
"""