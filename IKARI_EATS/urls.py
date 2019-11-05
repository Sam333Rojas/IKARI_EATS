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


from client.views import search_view, home_view, active_view, c_sales_view, confirmation_view, restaurant_view, client_sign_in_view
from core.views import test_template, redirect_home, logout_view
from authentication.views import login, reg_restaurant
from dealer.views import current, dealer_h, dealer_sign_in_view
from project_test.views import linked_list_test, python_list_test
from restaurant.views import items_view, item_view, active_sales, old_sales, restaurant_sign_in_view

urlpatterns = [
    path('', redirect_home),
    path('admin/', admin.site.urls),
    path('test/', test_template),
    path('login/', login, name='login'),
    path('search/', search_view),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('active_purchase/', active_view),
    path('client_sales/', c_sales_view),
    path('confirmation/', confirmation_view),
    path('restaurant/<int:restaurant_id>', restaurant_view, name='restaurant'),
    path('order/', current, name ='current'),
    path('dealer_home/', dealer_h),
    path('items/', items_view),
    path('item/<int:item_id>/', item_view, name='item'),
    path('active_sales/', active_sales),
    path('restaurant_sales/', old_sales),
    path('test/linked_list/<int:n>', linked_list_test),
    path('test/python_list/<int:n>', python_list_test),
    path('registration/restaurant', restaurant_sign_in_view, name="reg_rest"),
    path('registration/client', client_sign_in_view, name="reg_client"),
    path('registration/deliverer', dealer_sign_in_view, name="reg_del"),

]
