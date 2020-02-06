from django.db import models
from rest_framework import serializers as ser


class TestObject(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DecimalField(decimal_places=120, max_digits=128,null=True)


class TestObjectSerializer(ser.ModelSerializer):
    class Meta:
        model = TestObject
        fields = ('id', 'time')
