from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import OcaOcl
from opstmt.models import Year, Company
from .serializers import OcaOclSerializer, CompanyOcaOclSerializer
# from rest_framework.permissions import IsAuthenticated

# Create your views here.
class GetOcaOclView(APIView):
    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        companies = company.years.all()
        return Response(CompanyOcaOclSerializer(companies, many=True).data)
    

class UpdateOcaOclView(APIView):
    def post(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
        
        companies_data = request.data

        for company_data in companies_data:
            # Retrieve the company instance
            try:
                year = Year.objects.get(id=company_data['id'])
            except Year.DoesNotExist:
                return Response({'error': f'year with id {company_data["id"]} does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # Check if the token is authorized to update this company
            if year.company != company:
                return Response({'error': 'Unauthorized to update this company'}, status=status.HTTP_401_UNAUTHORIZED)

            # Retrieve the metrics data
            ocaocl_data = company_data.get('metrics')
            if not ocaocl_data:
                return Response({'error': 'Missing metrics data'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the opstmt instance associated with the company
            ocaocl = year.ocaocl

            # Deserialize and validate the opstmt data
            serializer = OcaOclSerializer(ocaocl, data=ocaocl_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'success', 'companies': request.data}, status=status.HTTP_200_OK)