from django.shortcuts import render, redirect
from profiles.models import ContractorProfile, UserProfile
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .forms import ContractorProfileForm, HomeOwnersEditForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def contractor_profile_view(request):
    if request.user.user_type != 'CO':
        return redirect('main:dashboard')
    
    # TODO add try and except to catch possible errors
    profile = ContractorProfile.objects.get(user = request.user)
    context = {
        'profile' : profile, 
        'loggedInUser' : 'contractor'
    }
    return render(request, 'user/contractor_home.html', context)


# refactored this view so that only one view handles all the edit profile for differennt users
@login_required
def editProfile(request):
    user = request.user
   
    # render CO edit page if user type is CO
    if request.user.user_type == 'CO':    
        return render(request, 'user/editprofiles/edit_profile.html', {})
    
    # elif request.user.user_type == 'AG':    
    #     return render(request, 'user/editprofiles/edit_profile.html', {})

    # render HO edit page if user type is HO
    elif request.user.user_type == 'HO': 
        user_objects = UserProfile.objects.get(user = user.id)
        return render(request, 'user/editprofiles/home_owners_edit_profile.html', {"details":user_objects})
    else:
        return redirect('main:dashboard')


def editHomeOwnerProfileRequest(request):
    try:
        user_profile = request.user.user_profile
    except UserProfile.DoesNotExist:
        # If the user profile doesn't exist, create a new one
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = HomeOwnersEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('main:home')
        else:
            messages.error(request, 'Profile update failed. Please correct the errors below.')
            return redirect('profile:edit-profile-request')
    else:
        form = HomeOwnersEditForm(instance=user_profile)    
    return render(request, 'profile/edit_profile.html', {'form': form})



# views.py
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = ContractorProfile
    form_class = ContractorProfileForm
    template_name = 'user/home_owners_edit_profile.html'
    
    def get_success_url(self):
        return reverse('profile:contractor_profile')

def editProfileRequest(request):
    user = request.user
    try:
        contractor_profile = ContractorProfile.objects.get(user=user.id)
    
        if request.method == 'POST':
            profile_form = ContractorProfileForm(request.POST, instance=contractor_profile)
            if profile_form.is_valid():
                profile_form.save()

                user.phone_number = profile_form.cleaned_data['phone_number']
                user.email = profile_form.cleaned_data['email']
                user.save()
                return redirect('profile:contractor_profile')
            else:
                print(profile_form.errors)
        else:
            profile_form = ContractorProfileForm(instance=contractor_profile)
    except ContractorProfile.DoesNotExist:
        # Redirect to profile creation page if profile doesn't exist
        return redirect('profile:edit-profile')

    return render(request, 'user/edit_profile.html', {'profile_form': profile_form})


@login_required
def search_view(request):
    context ={}
    return render(request, 'user/search_results.html', context)

@login_required
def search_view_results(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        results = []

        if query:
            # Perform search based on Title, Speciality, Email, and Phone number
            results = ContractorProfile.objects.filter(
                Q(user__username__icontains=query) |
                Q(specialization__icontains=query) |
                Q(user__phone_number__icontains=query)|
                Q(user__email__icontains=query) 
            )   
                
        return render(request, 'user/search_results.html', {'results': results})



@login_required
def upload_image(request):
    print(request.FILES)
    return redirect('profile:contractor_profile')