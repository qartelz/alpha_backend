from rest_framework import serializers
from .models import FF, Company, Year

class FFSerializer(serializers.ModelSerializer):
    class Meta:
        model = FF
        exclude = ['year', 'id']


class CompanyFFSerializer(serializers.ModelSerializer):
    metrics = FFSerializer(source='ff')  

    class Meta:
        model = Year
        fields = ['id','year', 'metrics']