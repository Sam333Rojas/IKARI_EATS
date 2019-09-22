"""IKARI_EATS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from client.views import search_view, home_view, active_view, c_sales_view, confirmation_view, restaurant_view
from restaurant.views import items_view
from core.views import test_template
from authentication.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_template),
    path('login/', login),
    path('search/', search_view),
    path('home/', home_view),
    path('active_purchase/', active_view),
    path('client_sales/', c_sales_view),
    path('confirmation/', confirmation_view),
    path('items/', items_view),
    path('restaurant/', restaurant_view),




]
