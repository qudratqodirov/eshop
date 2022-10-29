from django.db import models


# Таблица категории
class Category(models.Model):
    category_name = models.CharField(max_length=35)
    added_date = models.DateTimeField(auto_now_add=True)

    # Для нормального вида название
    def __str__(self):
        return self.category_name


# Таблица продуктов
class Product(models.Model):
    caregory_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=110)
    product_price = models.FloatField()
    product_desc = models.TextField()
    product_count = models.IntegerField()
    product_image = models.ImageField(upload_to='media', null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    # Для нормального вида название
    def __str__(self):
        return self.product_name


# Таблица Корзины
class UserCart(models.Model):
    user_id = models.IntegerField()
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_product_quantity = models.IntegerField()
    cart_date = models.DateTimeField(auto_now_add=True)

    # Для нормального вида название
    def __str__(self):
        return self.user_product

class ProductImages(models.Model):
    image = models.ImageField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return str(self.image)