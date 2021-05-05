from .models import Request, Friend
from .forms import EditProfile

def get_button(user, other_user):
    if Request.objects.filter(requester=user, requestee=other_user):
        button = "Cancel"
    elif Request.objects.filter(requester=other_user, requestee=user):
        button = "Accept"

    elif (Friend.objects.filter(user1=user, user2=other_user)) or (Friend.objects.filter(user2=user, user1=other_user)):
        button = "Unfriend"
    else:
        button = "Add"
    
    return button

def post_button_data(user, other_user, button):
    if button == "Add":
        button = "Cancel"
        Request.objects.create(requester=user, requestee=other_user)
    elif button == "Cancel":
        button = "Add"
        Request.objects.get(requester=user, requestee=other_user).delete()
    elif button == "Reject":
        button = "Add"
        Request.objects.get(requestee=user, requester=other_user).delete()

    elif button == "Accept":
        button = "Unfriend"
        Friend.objects.create(user1=user, user2=other_user)
        Request.objects.get(requestee=user, requester=other_user).delete()
    elif button == "Unfriend":
        button = "Add"
        try:
            friendship = Friend.objects.get(user1=user, user2=other_user)
        except Friend.DoesNotExist:
            friendship = Friend.objects.get(user2=user, user1=other_user)
        friendship.delete()
    
    return button

def save_form_data(request, profile):
    profile_bio = profile.bio
    profile_gender = profile.gender
    profile_address = profile.address

    posted_form = EditProfile(request.POST, files=request.FILES, instance=profile)
    if posted_form.is_valid():
        instance = posted_form.save(commit=False)
        instance.user = request.user
        if instance.bio == "":
            instance.bio = profile_bio
        if instance.gender == "":
            instance.gender = profile_gender
        if instance.address == "":
            instance.address = profile_address
        instance.save()

