from django.contrib.auth import authenticate ,login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
from client.models import Order, ClientSerializer, OrderSerializer
from core.views import prepare_parameters
from dealer.forms.dealer_form import DealerForm
from dealer.models import Dealer, DealerSerializer
from restaurant.models import Item, RestaurantSerializer


@login_required
def dealer_home_view(request, parameters):
    orders = Order.objects.filter(status=1)
    orders_serializer = OrderSerializer(orders, many=True)
    params = parameters
    params.update({
        'orders': orders_serializer.data,
    })
    # posicion dealer , hacer que se repita cada cierto tiempo mientras este en la  pagina
    """
    if request.method == 'POST':
        dealer = Dealer.objects.get(pk=request.user.id)
        dealer.latitude = request.POST.get('lat')
        dealer.longitude = request.POST.get('log')
        dealer.save()
        return HttpResponse(200)
    """
    return render(request, 'dealer_home.html', params)


"""
@login_required
def current(request,order_id):
    order_parameters = {}
    try:
        order = Order.objects.get(pk=order_id)
        restaurant_serializer = RestaurantSerializer(order.restaurant, many=False)
        client_serializer = ClientSerializer(order.client, many=False)
        dealer_serializer = DealerSerializer(order.dealer, many=False)
        order_parameters = {'item': {
            'id': order.id,
            'restaurant': restaurant_serializer.data,
            'client': client_serializer.data,
            'dealer': dealer_serializer.data,
        }}
        #dealer crea una solicitud
        sol = Solicitude.objects.create(dealer=order.dealer, order=order)
        sol.save()
    except Order.DoesNotExist:
        raise Http404()
    params = prepare_parameters(request)
    params.update(order_parameters)
    
    return render(request, 'current_order.html', params)
"""


@login_required
def current(request,item_id):
    item_parameters = {}
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
    """
    dealers = Dealers.objects.filter()
    dealers_serializer = DealerSerializer(restaurants, many=True)
    params.update({
        'dealers': dealers_serializer.data,
    })
    """
    return render(request, 'current_order.html', params)


@login_required
def dealer_h(request):
    return render(request, 'dealer_home.html', prepare_parameters(request))


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
        return render(request, 'reg_client.html', {'form': dealer_form})