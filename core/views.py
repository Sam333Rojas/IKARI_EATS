from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout


def test_template(request):
    return render(request, 'base.html')


def redirect_home(request):
    return HttpResponseRedirect(reverse('home'))


def logout_view(request):
    logout(request)
    return render(request, 'login.html')

