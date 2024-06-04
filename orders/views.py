from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test

from carts.models import Cart

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from .forms import OrderItemModelForm, OrderModelForm
from goods.models import Products

from django.contrib.auth import get_user_model


User = get_user_model()


def check_admin(user):
   return user.is_superuser


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        # Создать заказанные товары
                        for cart_item in cart_items:
                            product=cart_item.product
                            name=cart_item.product.name
                            price=cart_item.product.sell_price()
                            quantity=cart_item.quantity


                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {name} на складе\
                                                       В наличии - {product.quantity}')

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()

                        messages.success(request, 'Заказ оформлен!')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('cart:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'orders': True,
    }
    return render(request, 'orders/create_order.html', context=context)



@user_passes_test(check_admin)
def order_item_create(request):
    form = OrderItemModelForm(request.POST)
    orders = Order.objects.all()
    products = Products.objects.all()
    if form.is_valid():
        form.save()
        return redirect("/admin_panel")
    return render(request, 'admin_panel/order_item_create.html', {"products": products, "orders": orders})

@user_passes_test(check_admin)
def main_order_item(request):
    order_items = OrderItem.objects.all()
    return render(request, 'admin_panel/main_order_item.html', {"order_items": order_items})


def order_item_delete(request, id):
    instance = OrderItem.objects.get(id=id)
    instance.delete()
    return redirect("/orders/order_item_main/")


@user_passes_test(check_admin)
def order_item_edit(request, id):
    instance = OrderItem.objects.get(id=id)
    orders = Order.objects.all()
    products = Products.objects.all()

    if request.method == 'POST':
        form = OrderItemModelForm((request.POST or None), instance=instance)
        if form.is_valid():
            instance.save()
            return redirect("/orders/order_item_main")

    return render(request, 'admin_panel/order_item_create.html', {"order_item": instance, "products": products, "orders": orders})

@user_passes_test(check_admin)
def order_create(request):
    form = OrderModelForm(request.POST)
    users = User.objects.all()

    if form.is_valid():
        form.save()
        return redirect("/admin_panel")
    return render(request, 'admin_panel/order_create.html', {"users": users, "form": form})

@user_passes_test(check_admin)
def main_order(request):
    orders = Order.objects.all()
    return render(request, 'admin_panel/main_order.html', {"orders": orders})


def order_delete(request, id):
    instance = Order.objects.get(id=id)
    instance.delete()
    return redirect("/orders/order_main/")


@user_passes_test(check_admin)
def order_edit(request, id):
    instance = Order.objects.get(id=id)
    users = User.objects.all()

    if request.method == 'POST':
        form = OrderModelForm((request.POST or None), instance=instance)
        
        if form.is_valid():
            instance.save()
            return redirect("/orders/order_main")

    return render(request, 'admin_panel/order_create.html', {"users": users, "order": instance})