from django.db import models


class Slug(models.Model):
    slug = models.SlugField(verbose_name='Slug', unique=True, max_length=200)

    class Meta:
        abstract = True
