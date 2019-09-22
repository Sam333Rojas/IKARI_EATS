from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=12)


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=None, primary_key=True)
    rank = models.IntegerField()
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    address = models.CharField(max_length=100)
    tag = models.ForeignKey(Tag, on_delete=None)

    class Meta:
        db_table = 'restaurant'


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    description = models.TextField()
    path = models.CharField(max_length=64)
    name = models.CharField(max_length=12)
    tag = models.ForeignKey(Tag, on_delete=None)
    restaurant = models.ForeignKey(Restaurant, on_delete=None, related_name='items')
