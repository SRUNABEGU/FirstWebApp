from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField('наименование', max_length=50)
    description = models.CharField('описание', max_length=250)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('наименование', max_length=50)
    image = models.ImageField('изображение', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.FloatField('цена за покупку')
    description = models.CharField('описание', max_length=250, blank=True, default='')
    created_at = models.DateTimeField('дата создания')
    updated_at = models.DateTimeField('дата последнего изменения')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='владелец',
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
    )

    is_published = models.BooleanField('опубликован', default=False)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField('Имя', max_length=50)
    phone = models.CharField('Телефон', max_length=50)
    message = models.TextField('Сообщение', max_length=100)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.name} | {self.phone}"
