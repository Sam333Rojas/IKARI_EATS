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
                    'status': order.status,
                    'restaurant': {
                        'latitude': restaurant.latitude,
                        'longitude': restaurant.longitude,
                        'address': restaurant.address
                    },
                    'client': {
                        'latitude': client.latitude,
                        'longitude': client.longitude
                    },
                    'item': {
                        'name': order.item.name
                    }
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
        if order.status is not 2:
            time = request.POST.get('time')
            Solicitude.objects.create(order=order, time=time, dealer_id=request.user.id)
        return HttpResponse(200)


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
