from rest_framework import serializers
from .models import Papers

class PapersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Papers
        fields = (
            'id',
            'name',
            'author',
            'abstract',
        )