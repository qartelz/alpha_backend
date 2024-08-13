from rest_framework import serializers
from .models import WcTl, Company, Year

class WctlSerializer(serializers.ModelSerializer):
    class Meta:
        model = WcTl
        exclude = ['year', 'id']


class CompanyWcTlSerializer(serializers.ModelSerializer):
    metrics = WctlSerializer(source='wctl')  

    class Meta:
        model = Year
        fields = ['id','year', 'metrics']