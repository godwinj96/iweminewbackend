from rest_framework import serializers
from .models import *

class PapersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Papers
        fields = (
            'id',
            'name',
            'author',
            'abstract',
            'cover_page',
            'type',
            'category',
            'subcategory',
            'year_published',
        )

class TypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = (
            'id',
            'name',
        )

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'type',
        )

class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = (
            'id',
            'name',
            'type',
            'category',
        )