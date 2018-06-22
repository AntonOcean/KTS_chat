from django.contrib import admin

from chat.models import Message, User, Room


class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'text']
    search_fields = ['author__username', 'text']

admin.site.register((Message, User, Room))