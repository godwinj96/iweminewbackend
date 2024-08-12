from django.shortcuts import render
from django.db.models import Q

from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework.exceptions import NotFound


class PaperList(generics.ListCreateAPIView):
    serializer_class = PapersListSerializer

    def get_queryset(self):
        return Papers.objects.all()


from rest_framework import generics
from rest_framework.exceptions import NotFound
from .models import Papers
from .serializers import PapersListSerializer

class PaperDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PapersListSerializer
    lookup_field = 'name'

    def get_object(self):
        name = self.kwargs.get('name').replace('_', ' ')
        # Case-insensitive lookup for the paper name
        obj = Papers.objects.filter(name__iexact=name).first()
        if obj is None:
            raise NotFound(detail="Paper not found")
        return obj


class TypeList(generics.ListCreateAPIView):
    serializer_class = TypeListSerializer

    def get_queryset(self):
        return Type.objects.all()


class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TypeListSerializer
    lookup_field = 'name'

    def get_queryset(self):
        name = self.kwargs.get('name').replace('_', ' ')
        return Type.objects.filter(name=name)


class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return Category.objects.all()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryListSerializer
    lookup_field = 'name'

    def get_queryset(self):
        name = self.kwargs.get('name').replace('_', ' ')
        return Category.objects.filter(name=name)


class SubCategoryList(generics.ListCreateAPIView):
    serializer_class = SubCategoryListSerializer

    def get_queryset(self):
        return SubCategory.objects.all()


class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubCategoryListSerializer
    lookup_field = 'name'

    def get_queryset(self):
        name = self.kwargs.get('name').replace('_', ' ')
        return SubCategory.objects.filter(name=name)
