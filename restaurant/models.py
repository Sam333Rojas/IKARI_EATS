from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=12)


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=None, primary_key=True)
    rank = models.IntegerField()
    description = models.TextField()
    latitude = models.DecimalField(decimal_places=120, max_digits=128, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=120, max_digits=128, null=True, blank=True)
    address = models.CharField(max_length=100)
    tag = models.ForeignKey(Tag, on_delete=None)

    class Meta:
        db_table = 'restaurant'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['label']


class RestaurantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Restaurant
        fields = ['user_id', 'rank', 'latitude', 'longitude', 'address', 'tag', 'user', 'description']


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    description = models.TextField()
    path = models.CharField(max_length=64)
    name = models.CharField(max_length=12)
    tag = models.ForeignKey(Tag, on_delete=None)
    restaurant = models.ForeignKey(Restaurant, on_delete=None, related_name='items')


class ItemSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    restaurant = RestaurantSerializer()

    class Meta:
        model = Item
        fields = ('id', 'price', 'description', 'path', 'name', 'tag', 'restaurant')
