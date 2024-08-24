from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import *
from .serializers import *

from rest_framework import (generics, status)
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class PaperList(generics.ListCreateAPIView):
    serializer_class = PapersListSerializer

    def get_queryset(self):
        return Papers.objects.all()



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
    

### Public API 

class PaperListAPI(generics.ListCreateAPIView):
    serializer_class = PapersListSerializer
    queryset = Papers.objects.all()
    lookup_field = 'uploaded_by'


class MultipleFieldLookupORMixin(object):

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            try:                                  # Get the result with one or more fields.
                filter[field] = self.kwargs[field]
            except Exception:
                pass
        return get_object_or_404(queryset, **filter)  # Lookup the object

class PaperDetailAPI(MultipleFieldLookupORMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PapersListSerializer
    lookup_field = ('name', 'uploaded_by')

    def get_object(self):
        name = self.kwargs.get('name').replace('_', ' ')
        uploaded_by = self.kwargs.get('uploaded_by') or None
        if uploaded_by != None:
            # Case-insensitive lookup for the paper name
            obj = Papers.objects.filter(name__iexact=name, uploaded_by=uploaded_by).first()
            if obj is None:
                raise NotFound(detail="Paper not found")
            return obj
        else:
            return Response({"error": "user id not provided"}, status=status.HTTP_400_BAD_REQUEST)


