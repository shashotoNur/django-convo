import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from django.utils import timezone

from .models import Thread, ChatMessage, MessageStatus
from users.models import User


class ChatConsumer(AsyncConsumer):

    @database_sync_to_async
    def get_thread(self, user, other_user):
        user = User.objects.get(username=user)
        other_user = User.objects.get(username=other_user)
        self.user = user
        self.other_user = other_user
        try:
            thread = Thread.objects.get(user1=user, user2=other_user)
        except Thread.DoesNotExist:
            thread, created = Thread.objects.get_or_create(user2=user, user1=other_user)
        return thread

    @database_sync_to_async
    def create_chat_message(self, sender, msg):
        thread = self.thread
        present_time = timezone.now()

        ChatMessage.objects.create(thread=thread, sender=sender, message=msg, timestamp=present_time)

        status, created = MessageStatus.objects.get_or_create(thread=thread, user=self.other_user)

        if(status.last_online < status.last_offline) and (status.last_offline < present_time):
            new_msg_for = self.other_user
        else:
            new_msg_for = None

        thread.last_msg_time = present_time
        thread.new_msg_for = new_msg_for
        thread.save()

    @database_sync_to_async
    def update_user_status(self, user, field):
        thread = self.thread
        status, created = MessageStatus.objects.get_or_create(thread=thread, user=user)

        if field == 'online':
            status.last_online = timezone.now()
        elif field == 'offline':
            status.last_offline = timezone.now()
        status.save()
        self.status = status

        if thread.new_msg_for == user:
            thread.new_msg_for = None
            thread.save()


    # socket functions ----------------------------------------------------------------------
    async def websocket_connect(self, event):
        user = self.scope['user']
        other_user = self.scope['url_route']['kwargs']['other_username']

        thread = await self.get_thread(user, other_user)
        self.thread = thread
        self.thread_id = thread.id
        chat_room = f"thread_{self.thread_id}"
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.send({
            "type" : "websocket.accept"
        })

        await self.update_user_status(user, field='online')


    async def send_data(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })


    async def websocket_receive(self, event):
        event_text = event.get('text', None)
        if event_text is not None:
            user = self.user
            event_text_dict = json.loads(event_text)
            msg = event_text_dict.get('message')

            if msg:
                await self.create_chat_message(user, msg)

                recievedMsgDetails = {
                    'message': msg,
                    'username': user.username
                }

                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type": "send_data",
                        "text": json.dumps(recievedMsgDetails)
                    }
                )


    async def websocket_disconnect(self, event):
        user = self.scope['user']
        await self.update_user_status(user, field='offline')

        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )