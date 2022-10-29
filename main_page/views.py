from django.shortcuts import render, redirect
from django.http import HttpResponse

import telebot

from . import models

bot = telebot.TeleBot("5526002238:AAH7XxaGK7oAWZ-ZYEdXYv_OF5QNQD4KJ-U", parse_mode=None)


# Create your views here.

def home_page(request):
    all_category = models.Category.objects.all()  # Получить все категории из базы
    all_products = models.Product.objects.all()
    return render(request, 'index.html',
                  {'all_products': all_products, 'all_category': all_category})  # Передать на FRONT


# Получаем все товары и вывод их на Front
def get_all_products(request):
    all_products = models.Product.objects.all()  # Получить все продукты из базы
    all_category = models.Category.objects.all()
    return render(request, 'products.html', {
        'all_products': all_products,
        'all_category': all_category
    })  # Передать на FRONT


# Получение конкретного товара
def get_exect_product(request, pk):
    current_product = models.Product.objects.get(
        product_name=pk)  # Получить один продукт из базы (pk передаём название продукта)
    all_category = models.Category.objects.all()
    return render(request, 'single-product.html',
                  {
                      'current_product': current_product,
                      'all_category': all_category
                  })  # Передать на FRONT


# Получение товаров из категории
def get_exect_category(request, pk):
    # Получить данную категорию из базы (pk передаём название категории)
    current_category = models.Category.objects.get(id=pk)
    all_category = models.Category.objects.all()
    # Выводим продукты по категории
    category_product = models.Product.objects.filter(caregory_name=current_category)
    return render(request, 'category.html',
                  {
                      'current_category': current_category,
                      'category_product': category_product,
                      'all_category': all_category
                  })


# Поиск товара
def search_exect_product(request):
    if request.method == "POST":
        get_product = request.POST.get('search-product')  # search-product - name intupa
        try:
            models.Product.objects.get(product_name=get_product)

            return redirect(f'/product/{get_product}')
        except:
            return redirect('/')


# Добавление в корзину
def add_product_user_cart(request, pk):
    if request.method == 'POST':
        checker = models.Product.objects.get(id=pk)
        if checker.product_count >= int(request.POST.get('pr_count')):
            models.UserCart.objects.create(user_id=request.user.id, user_product=checker,
                                           user_product_quantity=int(request.POST.get('pr_count'))).save()
            return redirect(f'/products')
        else:
            return redirect(f'/product/{checker.product_name}')


# Корзина
def user_cart(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    count_products_in = len(user_cart)
    total = 0
    for checkout in user_cart:
        total += int(checkout.user_product_quantity) * float(checkout.user_product.product_price) + total

    all_category = models.Category.objects.all()
    return render(request, 'cart.html',
                  {'user_cart': user_cart, 'title': 'Корзина', 'all_category': all_category,
                   'count_products_in': count_products_in, 'total': total})  # Передать на FRONT


# Удаление продукта
def delete_exect_user_cart(request, pk):
    product_to_delete_product = models.Product.objects.get(id=pk)

    models.UserCart.objects.filter(user_id=request.user.id, user_product=product_to_delete_product).delete()

    return redirect('/user_cart')

# Оформление заказа
def checkout_page(request):
    checkout_cart_products = models.UserCart.objects.filter(user_id=request.user.id)
    total_price = 0
    text = '---------- Вы получили новый заказ с сайта -------------------------------\n '
    text += f'Имя: {request.POST.get("firstName")}\n ' \
            f'Фамилия: {request.POST.get("lastName")}\n ' \
            f'E-mail: {request.POST.get("email")}\n ' \
            f'Адрес: {request.POST.get("address")}\n ' \
            f'Адрес 2:{request.POST.get("address2")}\n ' \
            f'Адрес оплаты: {request.POST.get("same-address")}\n ' \
            f'Сохранить данные: {request.POST.get("save-info")}\n ' \
            f'Оплата: {request.POST.get("paymentMethod")}\n'

    text += '\n-------------- Заказынные товары --------------------\n'
    for checkout in checkout_cart_products:
        text += f'{checkout.user_product.product_name} - {checkout.user_product_quantity} x {checkout.user_product.product_price} = {checkout.user_product_quantity * checkout.user_product.product_price} \n'
        total_price += int(checkout.user_product_quantity) * float(checkout.user_product.product_price) + total_price
    admin_id = 1856086
    text += f'\n ---------- Общая сумма заказа---------------- \n {total_price}'
    bot.send_message(admin_id, text)

    models.UserCart.objects.filter(user_id=request.user.id).delete()
    return redirect('/')
