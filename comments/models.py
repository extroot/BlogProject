from django.db import models

from article.models import Article
from user.models import CustomUser


class Comment(models.Model):
    comment = models.CharField(verbose_name='Комментарий', max_length=2048)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='liking')
    item = models.ForeignKey(Article, on_delete=models.CASCADE,
                             verbose_name='Статья', related_name='liking')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
