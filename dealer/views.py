from django.contrib.auth import authenticate ,login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from core.views import prepare_parameters
from dealer.forms.dealer_form import DealerForm


@login_required
def current(request):
    return render(request, 'current_order.html', prepare_parameters(request))


@login_required
def dealer_h(request):
    return render(request, 'dealer_home.html', prepare_parameters(request))


def dealer_sign_in_view(request):
    dealer_form = DealerForm(request.POST or None)

    if request.method == 'POST':
        if dealer_form.is_valid():
            dealer = dealer_form.save()
            user = authenticate(request, username=dealer.user.username, password=dealer_form.cleaned_data['password'])
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                return render(request, 'login.html', {'error': True})
        else:
            #  TODO: Error
            pass
    else:
        return render(request, 'reg_client.html', {'form': dealer_form})