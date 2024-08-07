from django.shortcuts import render, redirect
from quotes.models import Project, QuoteRequest
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import AssignedAccount

User = get_user_model()

def agents_home_owner_account(request, pk):
    try:
        home_owner = User.objects.get(pk=pk)
        if not AssignedAccount.objects.filter(assigned_by = home_owner, assigned_to = request.user).exists():
            messages.error(request, f"you were not assigned by {home_owner.email} to view their account.")
            return  redirect('main:home')
        
        quotes = QuoteRequest.objects.filter(user=home_owner)
        quote = QuoteRequest.objects.filter(user=request.user)
        projects = Project.objects.filter(quote_request__user=home_owner)
        context = {
            "quotes": quotes,
            "quote": quote,
            "projects": projects,
            "quote_count": quotes.count(),
            "projects_count": projects.count(),
            "home_owner_id": pk
        }
        return render(request, 'user/home.html', context)
    except User.DoesNotExist:
        messages.error(request, 'Home Owner not found')
        return redirect('main:home')
        
def view_all_property(request):
    return render(request, 'user/all_property.html', {})     
    