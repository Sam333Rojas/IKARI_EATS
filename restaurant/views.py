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
def restaurant_home_view(request, params):
    restaurant_id = request.user.id
    restaurant_params = {}

    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        restaurant_params = {'restaurant': {
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
    params.update(restaurant_params)
    return render(request, 'rest_home.html', params)


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
        solicitude_serializer = SolicitudeSerializer(sol, many=True)
        # que el dealer no sea nulo en las orders
        orders = Order.objects.filter(restaurant=request.user, status=1)
        orders_ready = Order.objects.filter(restaurant=request.user, status=2)
        orders_serializer = OrderSerializer(orders, many=True)
        orders_ready_serializer = OrderSerializer(orders_ready, many=True)
        params = prepare_parameters(request)
        params.update({
            'solicitudes': solicitude_serializer.data,
            'orders': orders_serializer.data,
            'orders_ready': orders_ready_serializer.data,
        })
        return render(request, 'active_sales.html', params)
    else:
        try:
            order = Order.objects.get(pk=request.POST.get('order_id'))
            solicitude = Solicitude.objects.get(pk=request.POST.get('solicitude_id'))
            solicitude.status = 2
            order.status = 2
            order.save()
            return HttpResponse(200)
        except:
            return HttpResponse(400)


@login_required
def old_sales(request):
    return render(request, 'restaurant_sales.html', prepare_parameters(request))


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
