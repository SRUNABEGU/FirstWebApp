from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Add products to the database'

    def handle(self, *args, **kwargs):
        keyboards, _ = Category.objects.get_or_create(name='Клавиатуры')

        products = [
            {'name': 'Nuphy AIR75v2',
             'price': '13213',
             'category': 'keyboards',
             'created_at': '2026-07-25',
             'updated_at': '2026-07-25'},
            {'name': 'MCHOSE Jet 75',
             'price': '6270',
             'category': 'keyboards',
             'created_at': '2026-07-25',
             'updated_at': '2026-07-25'}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))
