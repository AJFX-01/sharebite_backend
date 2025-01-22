""" URLs """

from django.urls import path
from .views import (CancelPickupView, ReceiptHistoryView, RegisterView, LoginView,
                    DonationDetailView, DonationListView, ProofUploadView,
                    DropOffSiteView, ReserveDonationView, EditUserView,
                    ResetPasswordView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('edituser/', EditUserView.as_view(), name='edit-user'),
    path('resetpassword/', ResetPasswordView.as_view(), name='reset-password'),
    path('donations/', DonationListView.as_view(), name='donation-list'),
    path('donations/<int:donation_id>/proof/', ProofUploadView.as_view(), name='proof-upload'),
    path('dropoff-sites/', DropOffSiteView.as_view(), name='dropoff-sites'),
    path('donations/<int:donation_id>/reserve/', ReserveDonationView.as_view(),
         name='reserve-donation'),
    path('donations/<int:donation_id>/', DonationDetailView.as_view(), name='donation-detail'),
    path('receipts/', ReceiptHistoryView.as_view(), name='receipt-history'),
    path('donations/<int:donation_id>/cancel/', CancelPickupView.as_view(), name='cancel-pickup'),
]
