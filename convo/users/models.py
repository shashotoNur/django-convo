
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass


class Request(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="requester") # contains who has requested
    requestee = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="requestee") # contains who has a request
    seen      = models.BooleanField(default=False)


class Friend(models.Model):
    user1       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")


GENDER_CHOICES = (
    ('Prefer not to say','Prefer not to say'),
    ('Female', 'Female'),
    ('Male','Male'),
    ('Other','Other'),
)

class Profile(models.Model):
    name    = models.TextField(default='Unknown')
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    image   = models.ImageField(default='default_user.png', blank=True)
    bio     =  models.TextField(null=True, blank=True)
    gender  = models.CharField(max_length=20, null=True, blank=True, choices=GENDER_CHOICES, default=None)
    address = models.TextField(null=True, blank=True)