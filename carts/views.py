from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts
from django.contrib.auth.decorators import user_passes_test

from goods.models import Products
from .forms import CartModelForm
from django.contrib.auth import get_user_model


User = get_user_model()


def check_admin(user):
   return user.is_superuser


def cart_add(request):

    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(
                session_key=request.session.session_key, product=product, quantity=1)
    
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)
            

def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": cart}, request=request)

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
        "quaantity": updated_quantity,
    }

    return JsonResponse(response_data)



def cart_remove(request):
    
    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар удален",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)

@user_passes_test(check_admin)
def cart_create(request):
    form = CartModelForm(request.POST)
    goods = Products.objects.all()
    users = User.objects.all()
    if form.is_valid():
        form.save()
        return redirect("/admin_panel")
    return render(request, 'admin_panel/cart_create.html', {"goods": goods, "users": users})

@user_passes_test(check_admin)
def main_cart(request):
    carts = Cart.objects.all()
    return render(request, 'admin_panel/main_cart.html', {"carts": carts})


def cart_delete(request, id):
    instance = Cart.objects.get(id=id)
    instance.delete()
    return redirect("/cart/cart_main/")


@user_passes_test(check_admin)
def cart_edit(request, id):
    instance = Cart.objects.get(id=id)
    goods = Products.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        form = CartModelForm((request.POST or None), instance=instance)
        if form.is_valid():
            print(form.cleaned_data)
            instance.save()
            return redirect("/cart/cart_main")

    return render(request, 'admin_panel/cart_create.html', {"cart": instance, "goods": goods, "users": users})