from django.contrib.auth.models import User
from django.db import models


class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=None, primary_key=True)

    def __str__(self):
        return '{} <{}>'.format(self.user.first_name, self.user.id)

    class Meta:
        db_table = 'dealer'


"""
class DealerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Dealer
        fields = []
"""