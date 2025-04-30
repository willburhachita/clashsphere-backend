from django.contrib import admin
from chat.models import ChatRoom, ChatMessage

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('battle', 'created_at')
    search_fields = ('battle__title',)
    readonly_fields = ('created_at',)
    filter_horizontal = ('participants',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'room', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('sender__username', 'content', 'room__battle__title')
    readonly_fields = ('created_at',)
