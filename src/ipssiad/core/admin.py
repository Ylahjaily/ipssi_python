from django.contrib import admin, messages
from django.contrib.humanize.templatetags.humanize import naturaltime

from .models import (
    Profile,
    AdOfferProxy,
    AdRequestProxy,
    Category,
    Conversation,
    Message
)


@admin.register(Profile)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'company', 'updated', 'created']


class AdMixinAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'user', 'type', 'status', 'date_created']
    list_display_links = ['title', 'user']
    list_filter = ['type', 'status', 'user']
    ordering = ['created']
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'category')
        }),
        ('Options', {
            'fields': ('type', 'status')
        }),
        ('Dates', {
            'fields': ('created', 'updated')
        }),
    ]
    readonly_fields = ['created', 'updated']

    def date_created(self, obj):
        return naturaltime(obj.created)
    date_created.short_description = 'Date de création'

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        messages.add_message(request, messages.INFO, 'votre message')
        super(AdMixinAdmin, self).save_model(request, obj, form, change)


@admin.register(AdOfferProxy)
class AdOfferProxyAdmin(AdMixinAdmin):
    search_fields = ['title', 'description']

@admin.register(AdRequestProxy)
class AdRequestProxyAdmin(AdMixinAdmin):
    search_fields = ['title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ['title', 'slug', 'parent']
    prepopulated_fields = {'slug': ('title',), }


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['date_created']

    def date_created(self, obj):
        return naturaltime(obj.created)
    date_created.short_description = 'Date de création'



@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['uuid','status']
    inlines = [MessageInline]
