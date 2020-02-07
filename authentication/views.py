from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home/')
        return render(request, 'login.html', {'error': False})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return HttpResponseRedirect('/home/')
        else:
            return render(request, 'login.html', {'login_error': True})


def reg_restaurant(request):
    return render(request, 'reg_restaurant.html')


def reg_client(request):
    return render(request, 'reg_client.html')


def reg_deliverer(request):
    return render(request, 'reg_dealer.html')


def reg_item(request):
    return render(request, 'reg_item.html')


@login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login/')
