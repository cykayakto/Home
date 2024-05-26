from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    path('search/', views.catalog, name='search'),
    path('product/<slug:product_slug>/', views.product, name='product'),

    path('product_create/', views.product_create, name='product_create'),
    path("product_main/", views.main_product, name="main_product"),
    path("product_delete/<int:id>", views.product_delete, name="product_delete"),
    path("product_edit/<int:id>", views.product_edit, name="product_edit"),

    path('category_create/', views.category_create, name='category_create'),
    path("category_main/", views.main_category, name="main_category"),
    path("category_delete/<int:id>", views.category_delete, name="category_delete"),
    path("category_edit/<int:id>", views.category_edit, name="category_edit"),
    
    path('<slug:category_slug>/', views.catalog, name='index'),
]


