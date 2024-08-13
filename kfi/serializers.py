from rest_framework import serializers
from .models import KFI, Company, Year

class KfiSerializer(serializers.ModelSerializer):
    class Meta:
        model = KFI
        exclude = ['year', 'id']


class CompanyKfiSerializer(serializers.ModelSerializer):
    metrics = KfiSerializer(source='kfi')  

    class Meta:
        model = Year
        fields = ['id','year', 'metrics']