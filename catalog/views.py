from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from catalog.forms import ProductForm
from catalog.models import Product, Contact

from django.core.paginator import Paginator


def home(request):
    for product in Product.objects.order_by('-id')[:5]:
        print(f'ID: {product.id} | Название: "{product.name}" | Цена: {product.price}')

    product_list = Product.objects.order_by('-id')
    paginator = Paginator(product_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/home.html', {'page_obj': page_obj})


def about(request):
    return render(request, 'catalog/about.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def contacts(request):
    contact_data = Contact.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name}/{phone} отправил сообщение: "{message}"')

        return HttpResponse(f'Спасибо, {name}! Сообщение получено.')
    return render(request, 'catalog/contacts.html', {'contacts': contact_data})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_at = timezone.now()
            product.updated_at = timezone.now()
            product.save()
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})
