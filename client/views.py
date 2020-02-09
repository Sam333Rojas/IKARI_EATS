from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from client.forms.client_form import ClientForm
from client.models import Order, Client, ClientSerializer, OrderSerializer
from core.views import prepare_parameters
from restaurant.models import Restaurant, Item, RestaurantSerializer, ItemSerializer


@login_required
def search_view(request):
    if request.method != 'GET':
        return HttpResponseForbidden

    term = request.GET.get('term')
    restaurants = Restaurant.objects.filter(Q(user__first_name__icontains=term) | Q(tag__label__icontains=term))
    items = Item.objects.filter(
        Q(name__icontains=term) | Q(description__icontains=term) | Q(tag__label__icontains=term))
    restaurants_serializer = RestaurantSerializer(restaurants, many=True)
    items_serializer = ItemSerializer(items, many=True)

    params = prepare_parameters(request)
    params.update({
        'restaurants': restaurants_serializer.data,
        'items': items_serializer.data
    })

    return render(request, 'search.html', params)


@login_required
def active_view(request, item_id):
    try:
        current_order = Order.objects.get(status=1, client__user_id=request.user.id)
        if current_order is not None:
            params= {'error': True,
                     'error_type': "ya tienes una orden existente, se te proporcionara la informacion del pedido actual"
                     }
            return render(request, 'active_purchase.html', prepare_parameters(request), params)
    except:
        client = Client.objects.get(pk=request.user.id)
        client_serializer = ClientSerializer(client, many=False)
        item = Item.objects.get(pk=item_id)
        item_serializer = ItemSerializer(item,many=False)
        restaurant_id = item.restaurant.user.id
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        restaurant_serializer = RestaurantSerializer(restaurant, many=False)
        if client.latitude is not None:
            order = Order.objects.create(client=client, restaurant=restaurant, item=item)
            order_serializer = OrderSerializer(order, many=False)
            order.save()
            params = {
                'restaurant': restaurant_serializer.data,
                'client': client_serializer.data,
                'item': item_serializer.data,
                'error': False,
            }
        else:
            params = {'error': True,
                      'error_type': "usuario no tiene latitud ni longitud"}
        return render(request, 'active_purchase.html', prepare_parameters(request), params)


@login_required
def c_sales_view(request):
    return render(request, 'client_sales.html', prepare_parameters(request))


@login_required
def confirmation_view(request):
    return render(request, 'confirmation.html', prepare_parameters(request))


@login_required
def restaurant_view(request, restaurant_id):
    restaurant_parameters = {}
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        restaurant_parameters = {'restaurant': {
            'name': restaurant.user.first_name,
            'description': restaurant.description,
            'lat': restaurant.latitude,
            'log': restaurant.longitude,
            'address': restaurant.address,
            'items': [{
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
            } for item in restaurant.items.all()]
        }}
    except Restaurant.DoesNotExist:
        raise Http404()
    params = prepare_parameters(request)
    params.update(restaurant_parameters)
    return render(request, 'restaurant.html', params)


def client_sign_in_view(request):
    client_form = ClientForm(request.POST or None)

    if request.method == 'POST':
        if client_form.is_valid():
            client = client_form.save()
            user = authenticate(request, username=client.user.username, password=client_form.cleaned_data['password'])
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                return render(request, 'login.html', {'error': True})
        else:
            #  TODO: Error
            pass
    else:
        return render(request, 'reg_client.html', {'form': client_form})
