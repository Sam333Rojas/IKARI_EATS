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

from client.views import search_view, home_view, active_view, c_sales_view, confirmation_view, restaurant_view, \
    client_sign_in_view
from core.views import test_template, redirect_home
from authentication.views import login, reg_restaurant, reg_client
from dealer.views import current, dealer_h
from project_test.views import linked_list_test, python_list_test
from restaurant.views import items_view, item_view, active_sales, old_sales

urlpatterns = [
    path('', redirect_home),
    path('admin/', admin.site.urls),
    path('test/', test_template),
    path('login/', login, name='login'),
    path('search/', search_view),
    path('home/', home_view, name='home'),
    path('active_purchase/', active_view),
    path('client_sales/', c_sales_view),
    path('confirmation/', confirmation_view),
    path('restaurant/', restaurant_view),
    path('order/', current),
    path('dealer_home/', dealer_h),
    path('items/', items_view),
    path('item/', item_view),
    path('active_sales/', active_sales),
    path('restaurant_sales/', old_sales),
    path('test/linked_list/<int:n>', linked_list_test),
    path('test/python_list/<int:n>', python_list_test),
    path('registration/restaurant', reg_restaurant),
    path('registration/client', client_sign_in_view),

]
