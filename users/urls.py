from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('users-cart/', views.users_cart, name='users_cart'),
    path('logout/', views.logout, name='logout'),

    path('user_create/', views.user_create, name='user_create'),
    path("user_main/", views.main_user, name="main_user"),
    path("user_delete/<int:id>", views.user_delete, name="user_delete"),
    path("user_edit/<int:id>", views.user_edit, name="user_edit"),
    
]