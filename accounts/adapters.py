# adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.cache import cache
import uuid
from allauth.exceptions import ImmediateHttpResponse


class CustomAccountAdapter(DefaultAccountAdapter):
    # Customize account-related methods here
    pass

# custom_adapter.py
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin: SocialLogin):
        user = sociallogin.user

        if not user.id:  # If user doesn't exist yet
            # data = (sociallogin.serialize())
            # email = data['account']['extra_data']['email']
            existing_user = self.get_existing_user(user)
            if existing_user:
                sociallogin.connect(request, existing_user)
            else:
                sociallogin_key = str(uuid.uuid4())
                cache.set(sociallogin_key, sociallogin.serialize(), timeout=600)  # Store for 10 minutes
                request.session['sociallogin_key'] = sociallogin_key
                raise ImmediateHttpResponse(redirect(reverse("select_user_type")))

    def get_existing_user(self, user):
        # Assuming user.email is available and can be used to find existing user
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            return User.objects.get(email=user.email)
        except User.DoesNotExist:
            return None
        
    
    
    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        user_type = request.session.pop('user_type', None)
        if user_type:
            user.user_type = user_type
        return super(MySocialAccountAdapter, self).save_user(request, sociallogin, form)
    

# class MySocialAccountAdapter(DefaultAccountAdapter):
    #         else:
    #             sociallogin_key = str(uuid.uuid4())
    #             cache.set(sociallogin_key, sociallogin.serialize(), timeout=600)  # Store for 10 minutes
    #             request.session['sociallogin_key'] = sociallogin_key
    #             print('select_user_type')

    # def get_signup_redirect_url(self, request):
    #     print(23)
    #     print(request.user.user_type)
    #     sociallogin_key = request.session.get('sociallogin_key')
    #     sociallogin_data = cache.get(sociallogin_key)
    #     if request.user.user_type == '':
    #         print('lo')
    #         return reverse("select_user_type")
    #     # elif request.user.user_type == 'CO':
    #     #     return reverse("profile:contractor_profile")
        
    #     return super().get_signup_redirect_url(request)


    # def get_existing_user(self, user):
    #     # Check if a user with the given email already exists
    #     User = get_user_model()
    #     try:
    #         return User.objects.get(email=user.email)
    #     except User.DoesNotExist:
    #         return None

    # def save_user(self, request, sociallogin, form=None):
    #     user = sociallogin.user
    #     user_type = request.session.pop('user_type', None)
    #     if user_type:
    #         user.user_type = user_type
    #     return super(MySocialAccountAdapter, self).save_user(request, sociallogin, form)
