from django.contrib.auth import authenticate ,login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

# Create your views here.
from client.models import Order
from dealer.forms.dealer_form import DealerForm
from dealer.models import Dealer
from restaurant.models import Item


@login_required
def dealer_home_view(request,parameters):
    orders = Order.objects.filter(status=1)
    orders_serializer = OrderSerializer(orders, many=True)
    params = parameters
    params.update({
        'orders': orders_serializer.data,
    })
    return render(request, 'rest_home.html', params)




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