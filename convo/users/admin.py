from django.contrib import admin

from .models import User, Request, Friend, Profile

# Register your models here.
admin.site.register(User)
admin.site.register(Request)
admin.site.register(Friend)
admin.site.register(Profile)