from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Company, Opstmt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from assetnliabs.models import AssetnLiabs
from ocaocl.models import OcaOcl
from ratios.models import Ratios
from wctl.models import WcTl
from kfi.models import KFI
from ff.models import FF
from .models import Student, Year, Company, Opstmt
from .serializers import CompanySerializer, CompanyOpstmtSerializer, OpstmtSerializer, UserLoginSerializer
from ratios.views import calculate_ratios
from wctl.views import wl_tl_assmt_calculations
from kfi.views import kfi_calculations
from assetnliabs.views import assetnliabscalculation

# Create your views here.
class CreateCompanyView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        student = Student.objects.get(id=1)
        company_name = request.data.get('company_name')

        company = Company.objects.create(student=student, name=company_name)
        for year in range(2020, 2028):
            year = Year.objects.create(company=company, year=year)
            Opstmt.objects.create(year=year)
            AssetnLiabs.objects.create(year=year)
            OcaOcl.objects.create(year=year)
            Ratios.objects.create(year=year)
            WcTl.objects.create(year=year)
            KFI.objects.create(year=year)
            if year.year != 2020:
                FF.objects.create(year=year)

        return Response(CompanySerializer(company).data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCompaniesOpstmtView(APIView):
    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        years = company.years.all()
        return Response(CompanyOpstmtSerializer(years, many=True).data)
    

class UpdateCompaniesOpstmtView(APIView):
    def post(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

        companies_data = request.data

        for company_data in companies_data:
            # Ensure each company_data is a dictionary
            if not isinstance(request.data, list):
                return Response({'error': 'Expected a list of company data'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the company instance
            try:
                year = Year.objects.get(id=company_data['id'])
            except Year.DoesNotExist:
                return Response({'error': f'Year with id {company_data["id"]} does not exist'},
                                status=status.HTTP_404_NOT_FOUND)

            # Check if the token is authorized to update this company
            if year.company != company:
                return Response({'error': 'Unauthorized to update this company'}, status=status.HTTP_401_UNAUTHORIZED)

            # Retrieve the metrics data
            opstmt_data = company_data.get('metrics')
            if not opstmt_data:
                return Response({'error': 'Missing metrics data'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the opstmt instance associated with the company
            opstmt = year.opstmt

            # Deserialize and validate the opstmt data
            serializer = OpstmtSerializer(opstmt, data=opstmt_data)
            if serializer.is_valid():
                serializer.save()
                assetnliabscalculation(year.id)
                calculate_ratios(year.id)
                wl_tl_assmt_calculations(year.id)
                kfi_calculations(year.id)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'success', 'companies': request.data}, status=status.HTTP_200_OK)
