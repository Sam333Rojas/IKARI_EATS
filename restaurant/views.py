from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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