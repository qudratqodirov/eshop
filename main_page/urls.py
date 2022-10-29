from django.urls import path
from . import views

# Регистрация всех адресов сайта

urlpatterns = [
    path('', views.home_page),  # home_page название функции в файле views
    path('products', views.get_all_products),  # Ссылка на страницу продуктов
    path('product/<str:pk>', views.get_exect_product),  # Генерация динамический URL по имени продукта
    path('category/<int:pk>', views.get_exect_category),  # Генерация динамический URL по имени продукта
    path('search', views.search_exect_product),  # Поиск товара
    path('add_to_cart/<int:pk>', views.add_product_user_cart),  # Добавление товара в корзину
    path('user_cart', views.user_cart),  # Генерация динамический URL по имени продукта
    path('delete_product/<int:pk>', views.delete_exect_user_cart),  # Удаление товара
    path('checkout/', views.checkout_page)  # оформление заказа
]
