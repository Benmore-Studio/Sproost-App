from django import forms
from .models import ContractorProfile, UserProfile, AgentProfile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from address.forms import AddressField, AddressWidget
from django.contrib.auth import get_user_model
from main.models import Media

User = get_user_model()

class ContractorProfileForm(forms.ModelForm):
    # Defined phone_number and company_address fields as Django form fields
    phone_number = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US'))
    company_address = AddressField(
            widget=AddressWidget(attrs={'placeholder': 'Enter Address', 'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none mt-1 focus:border-gray-500'})
        )    
    email = forms.EmailField(required=False)
    class Meta:
        model = ContractorProfile
        fields = ['company_name', 'specialization', 'city', 'website',  'company_address', 'phone_number']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if email:
            user_id = self.instance.user.id if self.instance.user else None
            if User.objects.exclude(id=user_id).filter(email=email).exists():
                raise forms.ValidationError('This email address is already in use.')
        return email

class HomeOwnersEditForm(forms.ModelForm):
    phone_number = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US'))
    address = AddressField(
            widget=AddressWidget(attrs={'placeholder': 'Enter Address', 'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none mt-1 focus:border-gray-500'})
        )    
    email = forms.EmailField(required=False)
    class Meta:
        model = UserProfile
        fields = ['city', 'state_province', 'address', 'phone_number', 'email']


    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if email:
            user_id = self.instance.user.id if self.instance.user else None
            if User.objects.exclude(id=user_id).filter(email=email).exists():
                raise forms.ValidationError('This email address is already in use.')
        return email
    

class AgentEditForm(forms.ModelForm):
    phone_number = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US'))
    address = AddressField(
            widget=AddressWidget(attrs={'placeholder': 'Enter Address', 'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none mt-1 focus:border-gray-500'})
        )    
    email = forms.EmailField(required=False)
    class Meta:
        model = AgentProfile
        fields = ['address', 'phone_number', 'email', 'registration_ID' ]
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if email:
            user_id = self.instance.user.id if self.instance.user else None
            if User.objects.exclude(id=user_id).filter(email=email).exists():
                raise forms.ValidationError('This email address is already in use.')
        return email

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ContractorProfile
        fields = ['image']
