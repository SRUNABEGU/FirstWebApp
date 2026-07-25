from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product, Contact


def home(request):
    for product in Product.objects.order_by('id')[:5]:
        print(f'ID: {product.id} | Название: "{product.name}" | Цена: {product.price}')

    return render(request, 'catalog/home.html')


def about(request):
    return render(request, 'catalog/about.html')


def contacts(request):
    contact_data = Contact.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        print(f'{name}/{phone} отправил сообщение: "{message}"')

        return HttpResponse(f'Спасибо, {name}! Сообщение получено.')
    return render(request, 'catalog/contacts.html', {'contacts': contact_data})
