from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm


def profile(request):
    """ Displays user's profile. """

    # Getting the user's profile.
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Create a new instance(object) of the profile form, updating profile.
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            
    # User profile form as an instance to profile/user.
    form = UserProfileForm(instance=profile)
    # Getting profiles orders.
    # orders = profile.orders.all()
    template = 'profiles/profile.html'
    context = {
        'form': form,
        # 'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)
