from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=None, primary_key=True)

    '''to format the object'''
    def __str__(self):
        return '{} <{}>'.format(self.user.first_name, self.user.id)

    class Meta:
        db_table = 'client'
