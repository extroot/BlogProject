from datetime import datetime

from django.db import models
from tinymce.models import HTMLField

from core.models import Slug
from user.models import CustomUser


class Article(Slug):
    heading = models.CharField(verbose_name='Заголовок', max_length=64,
                               blank=True, null=True)
    text = HTMLField(verbose_name='Текст')
    visibility = models.BooleanField(verbose_name='Видимость')
    modified_date = models.DateTimeField(default=datetime.now())
    author = models.ForeignKey(
        verbose_name='Автор',
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='article'
    )
    tags = models.ManyToManyField(
        verbose_name='Теги',
        to='Tag',
        related_name='articles',
    )
    views_count = models.IntegerField(verbose_name='Просмотры')


class LikeDislike(models.Model):
    LIKING_CHOICES = [(1, 'like'), (0, 'neutral'), (-1, 'dislike')]
    liking = models.IntegerField('Оценка', default=0, null=True, blank=True,
                                 choices=LIKING_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='liking')
    item = models.ForeignKey(Article, on_delete=models.CASCADE,
                             verbose_name='Статья', related_name='liking')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        constraints = [
            models.UniqueConstraint(
                name='rating_unique',
                fields=('item', 'user')
            )
        ]
