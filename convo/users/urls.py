
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path("", views.index, name="index"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("search", views.search, name="search"),
    path("friends", views.friends, name="friends"),
    path("requests", views.requests, name="requests"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("notifications", views.notifications, name="notifications"),
]