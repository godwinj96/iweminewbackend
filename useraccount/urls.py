from django.urls import path, include, re_path
from .views import *
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Custom registration view
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', CustomRegisterView.as_view(), name='rest_register'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),

    path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
         VerifyEmailView.as_view(), name='account_confirm_email'),
    
    # Auth-related views
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    
    # Token management
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User details
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),

    # Account management from django-allauth
    path('account/', include('allauth.urls')),
]
