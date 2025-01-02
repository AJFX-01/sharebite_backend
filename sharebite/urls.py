from django.urls import path
from .views import RegisterView, LoginView, DonationDetailView, DonationListView, ProofUploadView, DropOffSiteView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('donations/', DonationListView.as_view(), name='donation-list'),
    path('donations/<int:pk>/', DonationDetailView.as_view(), name='donation-detail'),
    path('donations/<int:donation_id>/proof/', ProofUploadView.as_view(), name='proof-upload'),
    path('dropoff-sites/', DropOffSiteView.as_view(), name='dropoff-sites'),
]
