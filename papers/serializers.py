from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import Type

class TypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['name']

    def to_representation(self, instance):
        # Return the name of the type instead of the ID
        return instance.name

    def to_internal_value(self, data):
        # Return a dictionary with 'name' as the key and the data as the value
        return {'name': data}
    





class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def to_representation(self, instance):
        # Return the name of the category as a string
        return instance.name

    def to_internal_value(self, data):
        # Ensure that only the name is passed as a dictionary key
        if isinstance(data, str):
            return {'name': data}
        raise serializers.ValidationError("Invalid data. Expected a string representing the category name.")
    



class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name']

    def to_representation(self, instance):
        # Return the name of the subcategory instead of the ID
        return instance.name

    def to_internal_value(self, data):
        # Return a dictionary with 'name' as the key and the data as the value
        return {'name': data}


from rest_framework import serializers
from .models import Papers, Type, Category, SubCategory

class PapersListSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field='name', queryset=Type.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    subcategory = serializers.SlugRelatedField(slug_field='name', queryset=SubCategory.objects.all())
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Papers
        fields = '__all__'

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None

    def create(self, validated_data):
        # Directly use the instances from validated_data
        type_instance = validated_data.pop('type')
        category_instance = validated_data.pop('category')
        subcategory_instance = validated_data.pop('subcategory')

        paper = Papers.objects.create(
            type=type_instance,
            category=category_instance,
            subcategory=subcategory_instance,
            **validated_data
        )
        return paper

    def update(self, instance, validated_data):
        # Handle updating related fields
        if 'type' in validated_data:
            type_name = validated_data.pop('type')['name']
            instance.type = Type.objects.get(name=type_name)

        if 'category' in validated_data:
            category_name = validated_data.pop('category')['name']
            instance.category = Category.objects.get(name=category_name)

        if 'subcategory' in validated_data:
            subcategory_name = validated_data.pop('subcategory')['name']
            instance.subcategory = SubCategory.objects.get(name=subcategory_name)

        # Update the remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
