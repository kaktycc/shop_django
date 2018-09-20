from django.shortcuts import render, get_object_or_404
import datetime, random
from mainapp.models import ProductCategory, Product
from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def get_basket(request):
    if request.user.is_authenticated:
        return Basket.objects.filter(user=request.user)

def main(request):
    context = {
        'page_title': 'главная',
        'date_time': datetime.date.today,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/index.html', context)

def get_hot_product():
    products = Product.objects.filter(category__is_active = True, is_active = True)
    return random.sample(list(products), 1)[0]

def get_same_product(hot_product):
    same_products = Product.objects.filter(category=hot_product.category,category__is_active = True, is_active = True).exclude(pk=hot_product.pk)[:3]
    return same_products

def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)

    # basket = get_basket(request.user)
    basket = []
    # if request.user.is_authenticated:
    #     basket = Basket.objects.filter(user=request.user)
    #     # all_count, all_price = __count_price(Basket)


    if pk:
        if pk == '0':
            category = {'name': 'все', 'pk': 0}
            products = Product.objects.filter(category__is_active=True, is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'categories': links_menu,
            'category': category,
            'products': products_paginator,
            'basket': get_basket(request),
        }

        return render(request, 'mainapp/product_list.html', context)

    hot_product = get_hot_product()

    same_products = get_same_product(hot_product)

    context = {
        'page_title': 'каталог',
        'date_time': datetime.date.today,
        'basket': get_basket(request),
        'hot_product': hot_product,
        'same_product': same_products,
        'categories': links_menu,
    }

    return render(request, 'mainapp/catalog.html', context)


def contact(request):
    context = {
        'page_title': 'контакты',
        'date_time': datetime.date.today,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/contact.html', context)

def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    links_menu = ProductCategory.objects.all()
    context = {
        'date_time': datetime.date.today,
        'product': product,
        'categories': links_menu,
        'basket': get_basket(request),
    }

    return render(request, 'mainapp/product.html', context)