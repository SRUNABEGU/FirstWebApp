from django.db import models


class Product(models.Model):
    name = models.CharField('наименование', max_length=50)
    image = models.ImageField('изображение')
    category = models.CharField('категория', max_length=50)
    price = models.FloatField('цена за покупку')
    created_at = models.DateTimeField('дата создания')
    updated_at = models.DateTimeField('дата последнего изменения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    name = models.CharField('наименование', max_length=50)
    description = models.CharField('описание', max_length=250)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Contact(models.Model):
    phone = models.CharField('Телефон', max_length=50)
    email = models.EmailField('Email')
    address = models.TextField('Адрес', max_length=100)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.phone} | {self.email}"
