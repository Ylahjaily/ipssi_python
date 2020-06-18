import uuid

from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime

from .managers import AdOfferManager, AdRequestManager
from .utils import validate_file_extension, media_path


class Company(models.Model):
    """
    Model for profile company.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='Unique ID'
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Name'
    )
    phone = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Phone',
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name='Updated'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Created'
    )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Model for user profile.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='Unique ID'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    intro = models.TextField(
        verbose_name='Introduction',
        blank=True,
        null=True
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    avatar = models.FileField(
        upload_to=media_path,
        validators=[validate_file_extension],
        verbose_name='Avatar'
    )
    status = models.CharField(
        max_length=32,
        choices=(
            ('online', 'Online'),
            ('offline', 'Offline'),
        ),
        default='online'
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
        verbose_name = 'Profile'


class Address(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='Unique ID'
    )
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
    )
    address1 = models.CharField(
        max_length=255,
        blank=False
    )
    address2 = models.CharField(
        max_length=255,
        blank=True
    )
    postal_code = models.CharField(
        max_length=255,
        blank=False
    )
    city = models.CharField(
        max_length=255,
        blank=False
    )
    country = models.CharField(
        max_length=255,
        default='FR',
        verbose_name='Country',
        help_text='ISO Alpha-2'
    )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        indexes = [
            models.Index(fields=['address1', 'postal_code']),
        ]


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


class Ad(models.Model):
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
    description = models.TextField(
        verbose_name='Description',
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
    type = models.CharField(
        max_length=16,
        choices=(
            ('offer', 'Offre'),
            ('request', 'Demande'),
        ),
        default='offer',
        help_text='Annonce de type offer ou request'
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
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'
        unique_together = ['user', 'title']
        indexes = [
            models.Index(fields=['title', 'type'])
        ]

    def __str__(self):
        return '{} ({})'.format(self.title, self.user)

    @property
    def date_created(self):
        return naturaltime(self.created)


class AdOfferProxy(Ad):
    objects = AdOfferManager()

    class Meta:
        proxy = True
        verbose_name = 'Offre'


class AdRequestProxy(Ad):
    objects = AdRequestManager()

    class Meta:
        proxy = True
        verbose_name = 'Demande'


class OffersByUserProxy(Ad):
    objects = AdOfferManager()

    class Meta:
        proxy = True
        verbose_name = 'Offer of current user'


class RequestByUserProxy(Ad):
    objects = AdRequestManager()

    class Meta:
        proxy = True
        verbose_name = 'Request of current user'


class Conversation(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='Unique ID'
    )
    status = models.CharField(
        max_length=32,
        choices=(
            ('open', 'Open'),
            ('closed', 'Closed'),
        ),
        default='open',
        verbose_name='Status'
    )
    ad = models.ForeignKey(
        'Ad',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'


class Message(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='Unique ID'
    )
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.CASCADE,
    )
    transmitter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transmitter_message'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver_message'
    )
    content = models.TextField(
        verbose_name='Content',
    )
    read = models.BooleanField(
        verbose_name='Read',
        default=False
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Date de creation'
    )

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
