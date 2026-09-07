from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from catalog.forms import ProductForm
from catalog.models import Product, Contact


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = Product.objects.order_by('-id')
        for product in queryset[:5]:
            print(f'ID: {product.id} | Название: "{product.name}" | Цена: {product.price}')
        return queryset


class AboutView(TemplateView):
    template_name = 'catalog/about.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactsView(View):
    def get(self, request):
        contact_data = Contact.objects.first()
        return render(request, 'catalog/contacts.html', {'contacts': contact_data})

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name}/{phone} отправил сообщение: "{message}"')
        return HttpResponse(f'Спасибо, {name}! Сообщение получено.')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.created_at = timezone.now()
        product.updated_at = timezone.now()
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.updated_at = timezone.now()
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
