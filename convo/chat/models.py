
from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Thread(models.Model):
    user1           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='thread_user1')
    user2           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='thread_user2')
    new_msg_for     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='new_msg_for')
    last_msg_time   = models.DateTimeField(null=True)


class ChatMessage(models.Model):
    thread      = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="thread")
    sender      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    message     = models.TextField(default='[empty]')
    timestamp   = models.DateTimeField(default=timezone.now)


class MessageStatus(models.Model):
    thread          = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="msg_thread")
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='thread_user')
    last_online     = models.DateTimeField(default=timezone.now)
    last_offline    = models.DateTimeField(default=timezone.now)