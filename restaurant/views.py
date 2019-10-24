from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from restaurant.forms.restaurant_form import RestaurantForm


@login_required
def items_view(request):
    return render(request, 'items.html')


@login_required
def item_view(request, id):
    return render(request, 'item.html')


@login_required
def active_sales(request):
    return render(request, 'active_sales.html')


@login_required
def old_sales(request):
    return render(request, 'restaurant_sales.html')


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
            #  TODO: Error
            pass
    else:
        return render(request, 'reg_client.html', {'form': restaurant_form})