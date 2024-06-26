from django.urls import path
from . import views 


app_name = 'profile'
urlpatterns = [
    path('', views.contractor_profile_view, name='contractor_profile'),
    path('contractor-details/<int:pk>/', views.contractorDetails.as_view(), name='contractor_details'),
    path('edit-profile/', views.editProfile, name="edit-profile"),
    path('search-view/', views.search_view, name="search_contractor"),
    # path('search-view-results/', views.search_view_results, name="search-view-results"),
    path('contractor/update', views.ContractorProfileEditView, name="edit-contractor-profile"),
    path('home-owner/update', views.editHomeOwnerProfileRequest, name="edit-homeowners-profile"),
    path('agent/update', views.editAgentProfile, name="edit-agent-profile"),
    path('change-dp-request/', views.change_profile_pics_view, name="change-dp-request"),
    path('show-agent-menu/', views.show_agent_menu_view, name="show-agent-menu"),
    path('show-agent-message/', views.show_agent_message_view, name="show-agent-message"),
    path('update_onboarding_status/', views.update_onboarding_status, name="update_onboarding_status"),
]