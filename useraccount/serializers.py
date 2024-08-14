from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=255)
    # avatar = serializers.ImageField(upload_to="uploads/avatars/" null=True, blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['name'] = self.validated_data.get('name', '')
        return data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name' 'avatar', 'education', 'institution']