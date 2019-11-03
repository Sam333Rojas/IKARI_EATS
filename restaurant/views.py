from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from core.views import prepare_parameters
from restaurant.forms.restaurant_form import RestaurantForm


@login_required
def items_view(request):
    return render(request, 'items.html', prepare_parameters(request))


@login_required
def item_view(request, id):
    return render(request, 'item.html', prepare_parameters(request))


@login_required
def active_sales(request):
    return render(request, 'active_sales.html', prepare_parameters(request))


@login_required
def old_sales(request):
    return render(request, 'restaurant_sales.html', prepare_parameters(request))


def restaurant_sign_in_view(request):
    restaurant_form = RestaurantForm(request.POST or None)

    if request.method == 'POST':
        if restaurant_form.is_valid():
            restaurant = restaurant_form.save()
            user = authenticate(request, username=restaurant.user.username, password=restaurant_form.cleaned_data['password'])
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                return render(request, 'login.html', {'error': True})
        else:
            return HttpResponseRedirect('/login/')
    else:
        return render(request, 'reg_restaurant.html', {'form': restaurant_form})
