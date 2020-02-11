from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render

from client.models import Order, OrderSerializer
from core.views import prepare_parameters
from dealer.models import SolicitudeSerializer, Solicitude
from restaurant.forms.item_form import ItemForm
from restaurant.forms.restaurant_form import RestaurantForm
from restaurant.models import Item, Restaurant


@login_required
def items_view(request):
    return render(request, 'items.html', prepare_parameters(request))


# modificado
@login_required
def item_view(request, item_id):
    item_parameters = {}
    try:
        item = Item.objects.get(pk=item_id)
        item_parameters = {'item': {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
        }}
    except Item.DoesNotExist:
        raise Http404()
    params = prepare_parameters(request)
    params.update(item_parameters)
    return render(request, 'ritem.html', params)


@login_required
def active_sales(request):
    if request.method == 'GET':
        sol = Solicitude.objects.raw("""
    SELECT *
      FROM dealer_solicitude
     WHERE order_id IN (
                       SELECT id
                         FROM client_order
                        WHERE restaurant_id={}
                       );
        """.format(request.user.id))
        orders = Order.objects.filter(restaurant_id=request.user.id, status=1)
        orders_ready = Order.objects.filter(restaurant_id=request.user.id, status=2)
        orders_data = [{
            'id': order.id,
            'restaurant': {
                'id': order.restaurant.user.id,
                'latitude': order.restaurant.latitude,
                'longitude': order.restaurant.longitude,
            },
            'client': {
                'id': order.client.user.id,
                'name': order.client.user.first_name,
                'latitude': order.client.latitude,
                'longitude': order.client.longitude,
            },
            'item':{'name':order.item.name}
        } for order in orders]
        orders_ready_data = [{
            'id': order.id,
            'restaurant': {
                'id': order.restaurant.user.id,
                'latitude': order.restaurant.latitude,
                'longitude': order.restaurant.longitude,
            },
            'client': {
                'id': order.client.user.id,
                'name': order.client.user.first_name,
                'latitude': order.client.latitude,
                'longitude': order.client.longitude,
            },
            'item':{'name':order.item.name}
        } for order in orders_ready]
        solicitude_data = [{
            'id': solicitude.id,
            'order': {
                'id': solicitude.order.id,
                'creation_date': solicitude.order.creation_date,
                'status': solicitude.order.status,
                'restaurant': {
                    'id': solicitude.order.restaurant.user.id,
                    'latitude': solicitude.order.restaurant.latitude,
                    'longitude': solicitude.order.restaurant.longitude,
                },
                'client': {
                    'id': solicitude.order.client.user.id,
                    'name': solicitude.order.client.user.first_name,
                    'latitude': solicitude.order.client.latitude,
                    'longitude': solicitude.order.client.longitude,
                },
                'item':{
                    'name': solicitude.order.item.name
                }
            },
            'dealer': {
                'id': solicitude.dealer.user.id,
                'name': solicitude.dealer.user.first_name,
                'latitude': solicitude.dealer.latitude,
                'longitude': solicitude.dealer.longitude,
            },
            'time': solicitude.time
        } for solicitude in sol]
        params = prepare_parameters(request)
        params.update({
            'solicitudes': solicitude_data,
            'orders': orders_data,
            'orders_ready': orders_ready_data,
        })
        return render(request, 'active_sales.html', params)
    else:
        try:
            order = Order.objects.get(pk=request.POST.get('order_id'))
            order.status = 2
            order.save()
            solicitude = Solicitude.objects.get(pk=request.POST.get('solicitude_id'))
            solicitude.status = 2
            solicitude.save()
            dealer = solicitude.dealer
            dealer.status = 2
            dealer.save()
            return HttpResponse(200)
        except:
            return HttpResponse(400)


@login_required
def old_sales(request):
    orders = Order.objects.all().filter(restaurant_id=request.user.id).order_by('-creation_date')
    orders_data = [{
        'id': order.id,
        'client': {
            'name': order.client.user.first_name,
        },
        'creation_date': order.creation_date,
        'item': order.item.name
    } for order in orders]
    params = prepare_parameters(request)
    params.update({
        'orders': orders_data,
    })
    return render(request, 'client_sales.html', params)

def restaurant_sign_in_view(request):
    restaurant_form = RestaurantForm(request.POST or None)

    if request.method == 'POST':
        if restaurant_form.is_valid():
            restaurant = restaurant_form.save()
            user = authenticate(request, username=restaurant.user.username,
                                password=restaurant_form.cleaned_data['password'])
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                return render(request, 'login.html', {'error': True})
        else:
            return HttpResponseRedirect('/login/')
    else:
        return render(request, 'reg_restaurant.html', {'form': restaurant_form})


def item_creation(request):
    item_form = ItemForm(request.POST or None, request=request)
    if request.method == 'POST':
        if item_form.is_valid():
            item = item_form.save()
            if item is not None:
                return HttpResponseRedirect('/home/')
            else:
                return render(request, 'reg_item.html', {'error': True})
        else:
            return render(request, 'reg_item.html', {'error': True})
    else:
        return render(request, 'reg_item.html', {'form': item_form})
