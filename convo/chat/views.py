
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from itertools import chain

from .models import Thread, ChatMessage
from users.models import User, Profile, Friend
from chat.models import MessageStatus


class ThreadDict:
  def __init__(self, profile, last_msg_time, new_msg):
    self.profile = profile
    self.last_msg_time = last_msg_time
    self.new_msg = new_msg


# Create your views here.
@login_required(login_url="users:login")
def chats(request):
    user = request.user

    threads = chain(Thread.objects.filter(user2=user).values('user1', 'last_msg_time', 'new_msg_for'), Thread.objects.filter(user1=user).values('user2', 'last_msg_time', 'new_msg_for'))

    thread_list = []
    for thread in threads:
        if thread['last_msg_time']:
            last_msg_time = thread.get('last_msg_time')
            user_id = thread.get('user1') if thread.get('user1') is not None else thread.get('user2')
            profile = Profile.objects.get(user__id=user_id)
            new_msg = True if thread['new_msg_for'] == user.id else False

            thread = ThreadDict(profile, last_msg_time, new_msg )
            thread_list.append(thread)

    thread_list.sort(key=lambda thread: thread.last_msg_time, reverse=True)

    return render(request, "chat/chats.html", {
        "threads": thread_list
    })


@login_required(login_url="users:login")
def chat(request, other_username):
    user = request.user
    other_user = User.objects.get(username=other_username)
    try:
        Friend.objects.get(user1=user, user2=other_user)
    except Friend.DoesNotExist:
        try:
            Friend.objects.get(user2=user, user1=other_user)
        except Friend.DoesNotExist:
            return HttpResponseForbidden()

    try:
        thread = Thread.objects.get(user1=user, user2=other_user)
    except Thread.DoesNotExist:
        thread, created = Thread.objects.get_or_create(user1=other_user, user2=user)

    chats = ChatMessage.objects.filter(thread=thread)
    ordered_chats = chats.order_by('timestamp') if chats else chats

    paginated_chats = Paginator(ordered_chats, 15)
    last_page = paginated_chats.num_pages
    page_number = request.GET.get('page', last_page)
    chats_page = paginated_chats.get_page(page_number)

    return render(request, "chat/chat.html", {
        "chats_page": chats_page,
        "user": user,
        "other_user": other_user,
        "last_page": last_page
    })
