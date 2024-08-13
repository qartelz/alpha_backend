from rest_framework import serializers
from .models import Ratios, Year

class RatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratios
        exclude = ['year', 'id']


class CompanyRatiosSerializer(serializers.ModelSerializer):
    metrics = RatiosSerializer(source='ratios')  

    class Meta:
        model = Year
        fields = ['id','year', 'metrics']