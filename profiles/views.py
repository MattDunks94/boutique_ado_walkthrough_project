from django.shortcuts import render, get_object_or_404

from .models import UserProfile
from .forms import UserProfileForm


def profile(request):
    """ Displays user's profile. """

    # Getting the user's profile.
    profile = get_object_or_404(UserProfile, user=request.user)
    # User profile form as an instance to profile/user.
    form = UserProfileForm(instance=profile)
    # Getting profiles orders.
    # orders = profile.orders.all()
    template = 'profiles/profile.html'
    context = {
        'form': form,
        # 'orders': orders,
    }

    return render(request, template, context)
