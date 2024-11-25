from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=34, verbose_name='Названия продукта')
    brand = models.CharField(max_length=24, verbose_name='Бренд')
    category = models.CharField(max_length=24, verbose_name='Категория')
    price = models.PositiveBigIntegerField(default=0, verbose_name='Цена')
    product_image = models.ImageField(upload_to='ProductImages/', blank=True, null=True, verbose_name='Фото продукта')
    sign = models.PositiveIntegerField(default=0, verbose_name='знак')

    def __str__(self):
        return f'{self.product_name} - {self.price}'
