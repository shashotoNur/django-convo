from django.contrib import admin

from .models import ChatMessage, Thread, MessageStatus

# Register your models here.
admin.site.register(ChatMessage)
admin.site.register(Thread)
admin.site.register(MessageStatus)