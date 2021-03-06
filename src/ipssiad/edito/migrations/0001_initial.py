# Generated by Django 3.0.5 on 2020-06-10 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Unique ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, help_text='Used to build the category URL.', max_length=255, unique=True, verbose_name='Slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date de creation')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='edito.Category')),
            ],
            options={
                'verbose_name': 'Catégorie',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Unique ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('content', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('status', models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], default='online', max_length=32)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date de creation')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='edito.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['title', 'status'], name='edito_artic_title_160019_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together={('user', 'title')},
        ),
    ]
