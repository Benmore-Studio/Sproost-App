from django.db import models
from accounts.models import User
from address.models import AddressField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'user_profile')
    address = models.CharField(max_length = 50, null = True, blank = True)
    city = models.CharField(max_length = 50, null = True, blank = True)
    state_province = models.CharField(max_length = 50, null = True, blank = True)    
    
    def __str__(self):
        return self.user.username


class ContractorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'contractor_profile')
    company_name = models.CharField(max_length = 255)
    registration_number = models.CharField(max_length = 225)
    specialization = models.CharField(max_length = 225, null = True, blank = True)
    company_address = AddressField()
    city = models.CharField(max_length = 50)
    
    
