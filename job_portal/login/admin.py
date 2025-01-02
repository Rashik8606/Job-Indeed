from django.contrib import admin
from .models import UserProfile
from .models import ChatMessage,JobVacancies

# Register your models here.

admin.site.register(UserProfile)


class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender', 'receiver', 'message', 'is_read']

admin.site.register(ChatMessage, ChatMessageAdmin)

admin.site.register(JobVacancies)
