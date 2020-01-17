import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout

from client.models import Order
from restaurant.models import Restaurant, RestaurantSerializer


def test_template(request):
    return render(request, 'base.html')


@login_required
def home_view(request):
    params = {'user_group': request.user.groups.first().name}
    if params['user_group'] == 'client':
        return render(request, 'home.html', params)
    elif params['user_group'] == 'restaurant':
        if request.method == 'GET':
            params.update({
                'restaurant': RestaurantSerializer(Restaurant.objects.get(pk=request.user.id)).data
            })
            return render(request, 'rest_home.html', params)
        elif request.method == 'POST':
            restaurant = Restaurant.objects.get(pk=request.user.id)
            restaurant.latitude = request.POST.get('lat')
            restaurant.longitude = request.POST.get('log')
            restaurant.save()
            return HttpResponse(200)
    elif params['user_group'] == 'dealer':
        orders = Order.objects.filter(status=1)
        orders_serializer = OrderSerializer(orders, many=True)
        params = parameters
        params.update({
            'orders': orders_serializer.data,
        })
        return render(request, 'rest_home.html', params)


def redirect_home(request):
    return HttpResponseRedirect(reverse('home'))


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def prepare_parameters(req):
    return {'user_group': req.user.groups.first().name}
