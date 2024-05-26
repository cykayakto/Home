from django.urls import path
from django.shortcuts import redirect, render

from carts import views

app_name = 'carts'

urlpatterns = [
    path('cart_add/', views.cart_add, name='cart_add'),
    path('cart_change/', views.cart_change, name='cart_change'),
    path('cart_remove/', views.cart_remove, name='cart_remove'),

    path('cart_create/', views.cart_create, name='cart_create'),
    path("cart_main/", views.main_cart, name="main_cart"),
    path("cart_delete/<int:id>", views.cart_delete, name="cart_delete"),
    path("cart_edit/<int:id>", views.cart_edit, name="cart_edit"),
]