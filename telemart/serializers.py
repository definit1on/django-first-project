from rest_framework import serializers
from .models import *

class MovieSerializer1(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = ['title', 'year', 'power',
                  'company', 'picture']