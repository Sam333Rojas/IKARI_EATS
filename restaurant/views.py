from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def items_view(request):
    return render(request, 'item.html')


@login_required
def item_view(request, id):
    # TODO: items template
    pass
