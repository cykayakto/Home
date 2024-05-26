from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),

    path('order_item_create/', views.order_item_create, name='order_item_create'),
    path("order_item_main/", views.main_order_item, name="main_order_item"),
    path("order_item_delete/<int:id>", views.order_item_delete, name="order_item_delete"),
    path("order_item_edit/<int:id>", views.order_item_edit, name="order_item_edit"),

    path('order_create/', views.order_create, name='order_create'),
    path("order_main/", views.main_order, name="main_order"),
    path("order_delete/<int:id>", views.order_delete, name="order_delete"),
    path("order_edit/<int:id>", views.order_edit, name="order_edit"),
    
]