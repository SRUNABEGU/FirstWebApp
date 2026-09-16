from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группы "Модератор продуктов" и "Контент-менеджер" с нужными правами'

    def handle(self, *args, **options):
        product_ct = ContentType.objects.get_for_model(Product)

        moderator_group, _ = Group.objects.get_or_create(name='Модератор продуктов')

        unpublish_perm = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=product_ct,
        )
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=product_ct,
        )
        moderator_group.permissions.set([unpublish_perm, delete_perm])
        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" готова'))

        try:
            from blog.models import Post
            post_ct = ContentType.objects.get_for_model(Post)

            manage_blog_perm, _ = Permission.objects.get_or_create(
                codename='manage_blog',
                name='Может управлять публикациями блога',
                content_type=post_ct,
            )
            content_manager_group, _ = Group.objects.get_or_create(name='Контент-менеджер')
            content_manager_group.permissions.set([manage_blog_perm])
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" готова'))
        except ImportError:
            self.stdout.write(self.style.WARNING(
                'Модель blog.Post не найдена — группа "Контент-менеджер" пропущена'
            ))
