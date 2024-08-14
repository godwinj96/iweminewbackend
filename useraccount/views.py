from django.shortcuts import render

# Create your views here.

from django.db import IntegrityError
from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions
from .models import User
from .serializers import ProfileSerializer

class CustomRegisterView(RegisterView):
    
    def perform_create(self, serializer):
        print("perform_create is called")
        try:
            serializer.save(self.request)
        except IntegrityError as e:
            print(f"IntegrityError caught: {str(e)}")
            raise ValidationError({"error": "This email is already in use."})
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise ValidationError({"error": "An unexpected error occurred."})
        


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
        
        