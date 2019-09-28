from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render
from restaurant.models import Restaurant, Item, RestaurantSerializer


@login_required
def search_view(request):
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
