from rest_framework import serializers
from .models import OcaOcl, Year

class OcaOclSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcaOcl
        exclude = ['year', 'id']


class CompanyOcaOclSerializer(serializers.ModelSerializer):
    metrics = OcaOclSerializer(source='ocaocl')  

    class Meta:
        model = Year
        fields = ['id','year', 'metrics']