from django.contrib.auth.models import User
from django.db import models


class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=None, primary_key=True)
    """ agregar lat , log y estado
    latitude = models.DecimalField(decimal_places=120, max_digits=128)
    longitude = models.DecimalField(decimal_places=120, max_digits=128)
    status = models.IntegerField()
    """
    def __str__(self):
        return '{} <{}>'.format(self.user.first_name, self.user.id)

    class Meta:
        db_table = 'dealer'


"""
class DealerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Dealer
        fields = ['user_id', 'latitude', 'longitude', 'user','status']
"""