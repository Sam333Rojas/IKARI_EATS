import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout

from client.models import Order, OrderSerializer, Client
from dealer.models import Dealer
from restaurant.models import Restaurant


def test_template(request):
    return render(request, 'base.html')


@login_required
def home_view(request):
    params = {'user_group': request.user.groups.first().name}
    if params['user_group'] == 'client':
        if request.method == 'GET':
            return render(request, 'home.html', params)
        elif request.method == 'POST':
            client = Client.objects.get(pk=request.user.id)
            client.latitude = request.POST.get('lat')
            client.longitude = request.POST.get('log')
            client.save()
            return HttpResponse(200)
        return render(request, 'home.html', params)
    elif params['user_group'] == 'restaurant':
        if request.method == 'GET':
            restaurant_id = request.user.id
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
        elif request.method == 'POST':
            restaurant = Restaurant.objects.get(pk=request.user.id)
            restaurant.latitude = request.POST.get('lat')
            restaurant.longitude = request.POST.get('log')
            restaurant.save()
            return HttpResponse(200)
    elif params['user_group'] == 'dealer':
        if request.method == 'GET':
            dealer_id = request.user.id
            try:
                dealer = Dealer.objects.get(pk=dealer_id)
                dealer_params = {'dealer': {
                    'name': dealer.user.first_name,
                    'status': dealer.status,
                    'lat': dealer.latitude,
                    'log': dealer.longitude,
                }}
            except Dealer.DoesNotExist:
                raise Http404()
            params = prepare_parameters(request)
            params.update(dealer_params)
            orders = Order.objects.all()
            orders_data = [{
                'name': order.restaurant.user.first_name,
                'address': order.restaurant.address,
                'status': order.status,
                'id': order.id
            } for order in orders]
            order_params = {
                'orders': orders_data,
            }
            params.update(order_params)
            return render(request, 'dealer_home.html', params)
        elif request.method == 'POST':
            dealer = Dealer.objects.get(pk=request.user.id)
            dealer.latitude = request.POST.get('lat')
            dealer.longitude = request.POST.get('log')
            dealer.save()
            return HttpResponse(200)
        return render(request, 'dealer_home.html', params)


def redirect_home(request):
    return HttpResponseRedirect(reverse('home'))


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def prepare_parameters(req):
    return {'user_group': req.user.groups.first().name}
