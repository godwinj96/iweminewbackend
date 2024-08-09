from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import *
from .serializers import PapersListSerializer

from rest_framework import generics


class PaperList(generics.ListCreateAPIView):
    serializer_class = PapersListSerializer

    def get_queryset(self):
        queryset = Papers.objects.all()

        return queryset
    
    
class PaperDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PapersListSerializer

    def get_queryset(self):
        queryset = Papers.objects.all()

        return queryset
    
    
class TypeList(generics.ListCreateAPIView):
    serializer_class = PapersListSerializer

    def get_queryset(self):
        queryset = Type.objects.all()

        return queryset
    
    
class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PapersListSerializer

    def get_queryset(self):
        queryset = Type.objects.all()

        return queryset
    
    
class CategoryList(generics.ListCreateAPIView):
    serializer_class = PapersListSerializer

    def get_queryset(self):
        queryset = Category.objects.all()

        return queryset
    
    
class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PapersListSerializer

    def get_queryset(self):
        queryset = Type.objects.all()

        return queryset
    