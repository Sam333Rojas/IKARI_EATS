from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout

#from client.views import client_home_view
from dealer.views import dealer_home_view
from restaurant.views import restaurant_home_view


def test_template(request):
    return render(request, 'base.html')


def home_view(request):
    parameters = prepare_parameters(request)
    if parameters['user_group'] == 'client':
        return client_home_view(request,parameters)
    elif parameters['user_group'] == 'restaurant':
        return restaurant_home_view(request,parameters)
    elif parameters['user_group'] == 'dealer':
        return dealer_home_view(request,parameters)

def redirect_home(request):
    return HttpResponseRedirect(reverse('home'))


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def prepare_parameters(request):
    return {'user_group': request.user.groups.first().name}
