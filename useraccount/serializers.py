from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from django.urls import reverse
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User, Orders
from django.conf import settings


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_verification_email(user):
    subject = 'Verify Your Email Address'
    html_message = render_to_string('registration/email_verification.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    # avatar = serializers.ImageField(upload_to="uploads/avatars/" null=True, blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        print("Cleaned Data:", data)
        data['name'] = self.validated_data.get('name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        print(data)
        return data
    
    # def save(self, *args, **kwargs):
    #     user = super().save(*args, **kwargs)
    #     user.name = self.validated_data.get('name')
    #     user.last_name = self.validated_data.get('last_name')
    #     user.save()
    #     print(user)
    #     return user
    

    def save(self, request):
        name = self.validated_data.get('name')
        last_name = self.validated_data.get('last_name')
        email = self.validated_data.get('email')
        password = self.validated_data.get('password1')

        print(f"Creating user with: name={name}, last_name={last_name}, email={email}")

        user = User.objects.create_user(
            name=name,
            last_name=last_name,
            email=email,
            password=password
        )

        print("User Created:", user)
        return user
    


class OrderSerializer(serializers.ModelSerializer):
    paper_name = serializers.CharField(source='paper.name', read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'user', 'paper_name', 'time_created', 'status']
        read_only_fields = ['user', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['name', 'last_name', 'email', 'avatar', 'education', 'institution', 'is_staff', 'is_publisher', 'orders']


import logging
logger = logging.getLogger(__name__)


# class CustomPasswordResetSerializer(PasswordResetSerializer):
#     def get_email_options(self):
#         """
#         Override this method to change the reset link in the email.
#         """
#         print("Using custom password reset serializer")
#         request = self.context.get('request')
#         frontend_url = "http://iweminewbackend.onrender.com/password-reset/confirm/"  # Your React frontend URL
#         return {
#             'html_email_template_name': 'registration/password_reset_email.html',
#             'extra_email_context': {
#                 'frontend_url': frontend_url
#             },
#             'subject': 'Reset Password'
#         }



from django.contrib.sites.shortcuts import get_current_site
from allauth.account.utils import (
    filter_users_by_email, user_pk_to_url_str, user_username
)
from allauth.utils import build_absolute_uri
from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from allauth.account import app_settings
from dj_rest_auth.serializers import PasswordResetSerializer, AllAuthPasswordResetForm

class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)
            uidb64 = user_pk_to_url_str(user)

             # Log the uidb64 and token
            print(f"UIDB64: {uidb64}")
            print(f"Token: {temp_key}")

            # Build the path using uid and token
            path = f"password-reset/confirm/{uidb64}/{temp_key}/"
            
            # Use your custom frontend URL here
            frontend_url = "https://iwemiresearch.org/"  # Replace with your actual frontend URL
            reset_url = f"{frontend_url}{path}"
            
            # Log the URLs for debugging purposes
            print(f"Frontend reset URL: {reset_url}")

            # Context to be passed to the email template
            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": reset_url,
                "request": request,
                "path": path,
            }

            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
                
            # Send the email
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )

        return self.cleaned_data['email']

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def validate_email(self, value):
        # Use the custom reset form
        self.reset_form = CustomAllAuthPasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        return value


# from allauth.account.signals import email_confirmation_sent

# print(email_confirmation_sent(request, confirmation, signup))