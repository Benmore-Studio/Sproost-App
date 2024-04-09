from django.urls import path, include
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='account_login'),
    # other urls...
]