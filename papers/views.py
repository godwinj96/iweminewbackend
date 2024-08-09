from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import *
from .serializers import *

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
    serializer_class = TypeListSerializer

    def get_queryset(self):
        queryset = Type.objects.all()

        return queryset
    
    
class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TypeListSerializer

    def get_queryset(self):
        queryset = Type.objects.all()

        return queryset
    
    
class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        queryset = Category.objects.all()

        return queryset
    
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        queryset = Type.objects.all()

        return queryset
    
class SubCategoryList(generics.ListCreateAPIView):
    serializer_class = SubCategoryListSerializer

    def get_queryset(self):
        queryset = SubCategory.objects.all()

        return queryset
    
    
class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubCategoryListSerializer

    def get_queryset(self):
        queryset = SubCategory.objects.all()

        return queryset
    