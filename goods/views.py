from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect

from goods.models import Products, Categories
from goods.utils import q_search
from .forms import ProductModelForm, CategoryModelForm


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    
    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

    context = {
        "title": "Home - Каталог",
        "goods": current_page,
        "slug_url": category_slug
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    context = {"product": product}

    return render(request, "goods/product.html", context=context)







def product_create(request):
    form = ProductModelForm(request.POST)
    categories = Categories.objects.all()
    if form.is_valid():
        form.save()
        return redirect("/admin_panel")
    return render(request, 'admin_panel/product_create.html', {"categories": categories})


def main_product(request):
    products = Products.objects.all()
    return render(request, 'admin_panel/main_product.html', {"products": products})


def product_delete(request, id):
    instance = Products.objects.get(id=id)
    instance.delete()
    return redirect("/catalog/product_main/")


def product_edit(request, id):
    instance = Products.objects.get(id=id)
    categories = Categories.objects.all()

    if request.method == 'POST':
        form = ProductModelForm((request.POST or None), instance=instance)
        print(form, form.is_valid())
        if form.is_valid():
            instance.save()
            return redirect("/catalog/product_main")

    return render(request, 'admin_panel/product_create.html', {"product": instance, "categories": categories})








def category_create(request):
    form = CategoryModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin_panel")
    return render(request, 'admin_panel/category_create.html', {"form": form})


def main_category(request):
    categories = Categories.objects.all()
    return render(request, 'admin_panel/main_category.html', {"categories": categories})


def category_delete(request, id):
    instance = Categories.objects.get(id=id)
    instance.delete()
    return redirect("/catalog/category_main/")


def category_edit(request, id):
    instance = Categories.objects.get(id=id)

    if request.method == 'POST':
        form = CategoryModelForm((request.POST or None), instance=instance)
        print(form, form.is_valid())
        if form.is_valid():
            instance.save()
            return redirect("/catalog/category_main")

    return render(request, 'admin_panel/category_create.html', {"category": instance})