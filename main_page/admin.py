from django.contrib import admin
from . import models
# Register your models here.
#Регистрация базы, чтобы админу быти доступны таблицы
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.UserCart)
admin.site.register(models.ProductImages)
