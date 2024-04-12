from django.shortcuts import render, redirect
from profiles.models import ContractorProfile
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

from profiles.services.contractor import ContractorService
from .forms import ContractorProfileForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required


def contractor_profile_view(request):
    if request.user.user_type != 'CO':
        return redirect('main:dashboard')
    
    if request.method == "POST":
        if request.FILES:
            media = request.FILES.getlist("upload-media")
            data = {
                "media": media
            }
            contractor_service = ContractorService(request=request)
            add_media, error = contractor_service.add_media(data)

            if error:
                messages.error(request, error)
            else:
                messages.success(request, add_media)
        else:
            messages.error(request, "No file found!")
        
        return redirect("profile:contractor_profile")
    
    
    # TODO add try and except to catch possible errors
    profile = ContractorProfile.objects.get(user = request.user)

    context = {
        'profile' : profile, 
        'loggedInUser' : 'contractor'
    }
    return render(request, 'user/contractor_home.html', context)


@login_required
def editProfile(request):
    if request.user.user_type != 'CO':
        return redirect('main:dashboard')
    
    return render(request, 'user/edit_profile.html', {})

# views.py
class EditProfileView(UpdateView):
    model = ContractorProfile
    form_class = ContractorProfileForm
    template_name = 'user/edit_profile.html'
    
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

    print("hooy")
    return render(request, 'user/edit_profile.html', {'profile_form': profile_form})


def search_view(request):
    context ={}
    return render(request, 'user/search_results.html', context)

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

