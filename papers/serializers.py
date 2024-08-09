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
            '__all__'
        )

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            '__all__'
        )

class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = (
            '__all__'
        )