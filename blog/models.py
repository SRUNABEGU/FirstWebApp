from django.db import models


class Post(models.Model):
    title = models.CharField('заголовок', max_length=150)
    content = models.TextField('содержимое')
    preview = models.ImageField('превью', upload_to='blog/previews/', blank=True, null=True)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    is_published = models.BooleanField('опубликовано', default=False)
    views_count = models.PositiveIntegerField('количество просмотров', default=0)

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title
