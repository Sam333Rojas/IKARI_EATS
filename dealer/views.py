from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
from client.models import Order, ClientSerializer, OrderSerializer
from core.views import prepare_parameters
from dealer.forms.dealer_form import DealerForm
from dealer.models import Dealer, DealerSerializer, Solicitude
from restaurant.models import Item, RestaurantSerializer


@login_required
def current(request, order_id):
    if request.method == 'GET':
        try:
            order = Order.objects.get(pk=order_id)
            restaurant = order.restaurant
            client = order.client
            order_parameters = {
                'order': {
                    'id': order.id,
                    'restaurant': {'latitude': restaurant.latitude, 'longitude': restaurant.longitude},
                    'client': {'latitude': client.latitude, 'longitude': client.longitude},
                }
            }
            dealer = Dealer.objects.get(pk=request.user.id)
            dealer_parameters = {
                'dealer': {'latitude': dealer.latitude, 'longitude': dealer.longitude},
            }
        except Order.DoesNotExist:
            raise Http404()
        params = prepare_parameters(request)
        params.update(order_parameters)
        params.update(dealer_parameters)
        return render(request, 'current_order.html', params)
    else:
        order = Order.objects.get(pk=order_id)
        time = request.POST.get('time')
        Solicitude.objects.create(order=order, time=time, dealer_id=request.user.id)
        return HttpResponse(200)


"""
@login_required
def current(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        item_parameters = {'item': {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'restaurant_lat': item.restaurant.latitude,
            'restaurant_log': item.restaurant.longitude,
        }}
    except Item.DoesNotExist:
        raise Http404()
    params = prepare_parameters(request)
    params.update(item_parameters)
    dealers = Dealer.objects.filter()
    dealers_serializer = DealerSerializer(dealers, many=True)
    params.update({
        'dealers': dealers_serializer.data,
    })
    return render(request, 'current_order.html', params)
"""


def dealer_sign_in_view(request):
    dealer_form = DealerForm(request.POST or None)

    if request.method == 'POST':
        if dealer_form.is_valid():
            dealer = dealer_form.save()
            user = authenticate(request, username=dealer.user.username, password=dealer_form.cleaned_data['password'])
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                return render(request, 'login.html', {'error': True})
        else:
            #  TODO: Error
            pass
    else:
        return render(request, 'reg_dealser.html', {'form': dealer_form})
