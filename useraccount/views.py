from django.shortcuts import render

# Create your views here.

from django.db import IntegrityError
from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions
from .models import User
from .serializers import *
from dj_rest_auth.views import PasswordResetView

# class CustomRegisterView(RegisterView):
#     serializer_class = CustomRegisterSerializer
    
#     def perform_create(self, serializer):
#         print("perform_create is called")
#         try:
#             serializer.save(self.request)
#         except IntegrityError as e:
#             print(f"IntegrityError caught: {str(e)}")
#             raise ValidationError({"error": "This email is already in use."})
#         except Exception as e:
#             print(f"Unexpected error: {str(e)}")
#             raise ValidationError({"error": "An unexpected error occurred."})
        
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def perform_create(self, serializer):
        print("Perform Create Called")
        print("Serializer Data:", serializer.validated_data)  # Debugging print
        try:
            user = serializer.save(self.request)
            print("User Created in View:", user)
        except IntegrityError as e:
            print(f"IntegrityError caught: {str(e)}")
            raise ValidationError({"error": "This email is already in use."})
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise ValidationError({"error": "An unexpected error occurred."})


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class CustomPasswordResetView(PasswordResetView):
    serializer_class = CustomPasswordResetSerializer
        


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Orders
from papers.models import Papers
from .serializers import OrderSerializer

class ProfileOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # Get the authenticated user
        order_status = request.data.get('status')
        paper_id = request.data.get('paper_id')  # Get the paper ID from the request body
        if not paper_id:
            return Response({"error": "Paper ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            paper = Papers.objects.get(id=paper_id)  # Get the paper object
        except Papers.DoesNotExist:
            return Response({"error": "Paper not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create a new order for the user
        order = Orders.objects.create(user=user, paper=paper, status=order_status)
        
        # Serialize the new order data and return a response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request):
        user = request.user  # Get the authenticated user
        order_status = request.data.get('status')
        paper_id = request.data.get('paper_id')  # Get the paper ID from the request body
        order_id = request.data.get('id')

        if not paper_id:
            return Response({"error": "Paper ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            paper = Papers.objects.get(id=paper_id)  # Get the paper object
        except Papers.DoesNotExist:
            return Response({"error": "Paper not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Assuming the order you want to update is unique to the user and paper combination
            order = Orders.objects.get(id=order_id)
            order.status = order_status
            order.save()
        except Orders.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)