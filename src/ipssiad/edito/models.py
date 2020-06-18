import uuid

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='Unique ID'
    )
    title = models.CharField(
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        blank=True,
        verbose_name='Slug',
        help_text='Used to build the category URL.'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Date de creation'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Catégorie'

    def __str__(self):
        return self.title


class Article(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='Unique ID'
    )
    title = models.CharField(
        max_length=255,
        unique=True
    )
    content = models.TextField(
        verbose_name='Content',
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=32,
        choices=(
            ('online', 'Online'),
            ('offline', 'Offline'),
        ),
        default='online',
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name='Date de modification'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Date de creation'
    )

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        unique_together = ['user', 'title']
        indexes = [
            models.Index(fields=['title', 'status'])
        ]

    def __str__(self):
        return '{} ({})'.format(self.title, self.user)
