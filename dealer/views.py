from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def current(request):
    return render(request, 'current_order.html')

@login_required
def dealer_h(request):
    return render(request, 'dealer_home.html')