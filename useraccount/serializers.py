from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from django.urls import reverse
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    # avatar = serializers.ImageField(upload_to="uploads/avatars/" null=True, blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['name'] = self.validated_data.get('name', '')
        return data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name', 'avatar', 'education', 'institution']

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        """
        Override this method to change the reset link in the email.
        """
        request = self.context.get('request')
        frontend_url = "http://iweminewbackend.onrender.com/password-reset/confirm/"  # Your React frontend URL
        return {
            'email_template_name': 'registration/password_reset_email.html',
            'extra_email_context': {
                'frontend_url': frontend_url
            }
        }