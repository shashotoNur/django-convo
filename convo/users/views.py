import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from itertools import chain
from django.utils import timezone

from .models import User, Request, Friend, Profile
from chat.models import Thread
from .forms import EditProfile
from .utils import get_button, post_button_data, save_form_data


# Create your views here.
def index(request):
    return render(request, "users/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("chat:chats"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "../templates/users/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:index"))


def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "users/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile.objects.create(user=user, name=name)
        except IntegrityError:
            return render(request, "users/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("chat:chats"))
    else:
        return render(request, "users/register.html")


def search(request):
    query = request.GET.get("q")

    if query:
        users = User.objects.filter(username__icontains=query)
        profiles = Profile.objects.filter(user__in=users)

        page_number = request.GET.get('page', 1)
        paginated_profiles = Paginator(profiles, 15).get_page(page_number)
        msg = "Searched for " + query

        return render(request, "users/profile_list.html", {
            "msg": msg,
            "paginated_profiles": paginated_profiles
        })

    else:
        return HttpResponseRedirect(reverse("chat:chats"))


@login_required(login_url="users:login")
def friends(request):
    user = request.user
    friends = chain(Friend.objects.filter(user2=user).values('user1'), Friend.objects.filter(user1=user).values('user2'))

    profiles = []
    for friend in friends:
        user_in = friend.get('user1') if friend.get('user1') is not None else friend.get('user2')
        profile = Profile.objects.get(user__id=user_in)
        profiles.append(profile)

    page_number = request.GET.get('page', 1)
    paginated_profiles = Paginator(profiles, 15).get_page(page_number)
    msg = "Start a chat!"

    return render(request, "users/profile_list.html", {
        "msg": msg,
        "paginated_profiles": paginated_profiles
    })


@login_required(login_url="users:login")
def requests(request):
    user = request.user
    chat_requests = Request.objects.filter(requestee=user)

    profiles = []
    for chat_request in chat_requests:
        chat_request.seen = True
        chat_request.save()
        profile = Profile.objects.get(user=chat_request.requester)
        profiles.append(profile)

    page_number = request.GET.get('page', 1)
    paginated_profiles = Paginator(profiles, 15).get_page(page_number)
    msg = "Chat requests"

    return render(request, "users/profile_list.html", {
        "msg": msg,
        "paginated_profiles": paginated_profiles
    })


@login_required(login_url="users:login")
@csrf_exempt
def profile(request, name):
    user = request.user
    other_user = User.objects.get(username=name)
    profile = Profile.objects.get(user=other_user)

    button = None
    form = None

    if request.method == "GET":
        if user != other_user:
            button = get_button(user, other_user)
        else:
            form = EditProfile()

    if request.method == "POST":
        try:
            button = json.loads(request.body).get('button')
            button = post_button_data(user, other_user, button)
            return JsonResponse({"button": button})

        except:
            save_form_data(request, profile)
            form = EditProfile()


    return render(request, "users/profile.html", {
        "other_user": other_user,
        "profile": profile,
        "button": button,
        "form": form
    })


@login_required(login_url="users:login")
def notifications(request):
    user = request.user
    new_req = 'false'
    new_msg = 'false'

    requests = Request.objects.filter(requestee=user)
    for request in requests:
        if request.seen == False:
            new_req = 'true'
            break
    
    users_with_new_msg = chain(Thread.objects.filter(user2=user).values('new_msg_for'), Thread.objects.filter(user1=user).values('new_msg_for'))
    for user_with_new_msg in users_with_new_msg:
        if user_with_new_msg['new_msg_for'] == user.id:
            new_msg = 'true'
            break

    return JsonResponse({"new_req": new_req, "new_msg": new_msg})