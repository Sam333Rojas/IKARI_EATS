from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def test_template(request):
    return render(request, 'base.html')

def redirect_home(request):
    return HttpResponseRedirect(reverse('home'))
