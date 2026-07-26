from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Add products to the database'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        keyboards, _ = Category.objects.get_or_create(
            name='Клавиатуры',
            defaults={'description': ''}
        )

        products = [
            {'name': 'Nuphy AIR75v2',
             'category': keyboards,
             'price': 13213,
             'created_at': '2026-07-25',
             'updated_at': '2026-07-25'},
            {'name': 'MCHOSE Jet 75',
             'category': keyboards,
             'price': 6270,
             'created_at': '2026-07-25',
             'updated_at': '2026-07-25'},
        ]

        for product_data in products:
            name = product_data.pop('name')
            category = product_data.pop('category')
            product, created = Product.objects.get_or_create(
                name=name,
                category=category,
                defaults=product_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
            # else:
            # self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))
