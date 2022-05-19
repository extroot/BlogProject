from django.contrib import admin

from article.models import Article, LikeDislike

admin.site.register(Article)
admin.site.register(LikeDislike)
