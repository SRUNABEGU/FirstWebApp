from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Contact, Category
from catalog.services import ProductService


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


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.created_at = timezone.now()
        product.updated_at = timezone.now()
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product = form.save(commit=False)
        product.updated_at = timezone.now()
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        is_owner = product.owner == request.user
        is_moderator = request.user.has_perm('catalog.delete_product')
        if not (is_owner or is_moderator):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied
        product.is_published = False
        product.save()
        return redirect('catalog:product_detail', pk=pk)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    login_url = 'users:login'
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        return ProductService.get_products_by_category(self.kwargs['category_id'])
