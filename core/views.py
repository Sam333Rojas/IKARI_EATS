from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout


def test_template(request):
    return render(request, 'base.html')


def redirect_home(request):
    return HttpResponseRedirect(reverse('home'))


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def prepare_parameters(request):
    return {'user_group': request.user.groups.first().name}
