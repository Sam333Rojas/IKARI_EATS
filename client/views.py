from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from client.forms.client_form import ClientForm
from restaurant.models import Restaurant, Item, RestaurantSerializer


@login_required
def search_view(request):
    if request.user.groups.filter(name='client').exists():
        ## Action if existing
        pass
    else:
        ## Chao
        pass
    if request.method != 'GET':
        return HttpResponseForbidden

    term = request.GET.get('term')
    restaurants = Restaurant.objects.filter(Q(user__first_name__icontains=term) | Q(tag__label__icontains=term))
    items = Item.objects.filter(name__icontains=term)
    restaurants_serializer = RestaurantSerializer(restaurants, many=True)
    """
    items_serializer = ItemSerializer(items)
    """
    return render(request, 'search.html', {
        'restaurants': restaurants_serializer.data
    })


@login_required
def home_view(request):
    return render(request, 'home.html')


@login_required
def active_view(request):
    return render(request, 'active_purchase.html')


@login_required
def c_sales_view(request):
    return render(request, 'client_sales.html')


@login_required
def confirmation_view(request):
    return render(request, 'confirmation.html')


@login_required
def restaurant_view(request):
    return render(request, 'restaurant.html')


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
