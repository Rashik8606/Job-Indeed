from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.models import UserProfile
from django.contrib import messages
from django.contrib.auth.models import User



@login_required
def profile(request):
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'user_profile': userprofile})



@login_required
def update_profile_pic(request):
    if request.method == 'POST' and request.FILES.get('profilepic'):
        user_profile = request.user.user_profile  # corrected attribute name
        user_profile.profile_picture = request.FILES['profilepic']  # corrected field name
        user_profile.save()
        messages.success(request, 'Profile picture updated successfully!')
        return redirect('profile')
    else:
        messages.error(request, 'Failed to update profile picture!')
        return redirect('profile')
    

def BackToPage(request):
        return redirect('index')


