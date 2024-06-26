from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from carts.models import Cart
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import user_passes_test
from .models import User

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm, UserModelForm
from django.utils.timezone import now


def check_admin(user):
   return user.is_superuser


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                    
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
    
    context = {
        'title': 'Home - Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профайл успешно обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")
        

    context = {
        'title': 'Home - Кабинет',
        'form': form,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context)

def users_cart(request):
    return render(request, 'users/users_cart.html')


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))


@user_passes_test(check_admin)
def user_create(request):
    form = UserModelForm(request.POST)
    users = User.objects.all()
    date = str(now())
    print(form.errors)


    if form.is_valid():
        form.save()
        return redirect("/admin_panel")
    return render(request, 'admin_panel/user_create.html', {"date": date, "form": form})

@user_passes_test(check_admin)
def main_user(request):
    users = User.objects.all()
    return render(request, 'admin_panel/main_user.html', {"users": users})

@user_passes_test(check_admin)
def user_delete(request, id):
    instance = User.objects.get(id=id)
    instance.delete()
    return redirect("/user/user_main/")

@user_passes_test(check_admin)
def user_edit(request, id):
    instance = User.objects.get(id=id)
    users = User.objects.all()
    date = str(instance.date_joined)
    print(date)


    if request.method == 'POST':
        form = UserModelForm((request.POST or None), instance=instance)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            instance.save()
            return redirect("/user/user_main")

    return render(request, 'admin_panel/user_create.html', {"date": date, "current_user": instance})