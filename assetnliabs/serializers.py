from rest_framework import serializers
from .models import AssetnLiabs, Company, Year

class AssetnLiabsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetnLiabs
        exclude = ['year', 'id']


class CompanyAssetnLiabsSerializer(serializers.ModelSerializer):
    metrics = AssetnLiabsSerializer(source='assetnliabs')  

    class Meta:
        model = Year
        fields = ['id','year', 'metrics']