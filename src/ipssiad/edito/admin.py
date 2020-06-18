from django.contrib import admin
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ['title', 'slug', 'parent']
    prepopulated_fields = {'slug': ('title',), }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'user', 'status']
    list_display_links = ['title', 'user']
    list_filter = ['status', 'user']
    ordering = ['created']
    fieldsets = [
        (None, {
            'fields': ('title', 'content', 'category')
        }),
        ('Options', {
            'fields': ('status', )
        }),
        ('Dates', {
            'fields': ('created', 'updated')
        }),
    ]
    readonly_fields = ['created', 'updated']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(ArticleAdmin, self).save_model(request, obj, form, change)
