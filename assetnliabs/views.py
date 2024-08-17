from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AssetnLiabs
from opstmt.models import Year, Company, Opstmt
from ocaocl.models import OcaOcl
from .serializers import AssetnLiabsSerializer, CompanyAssetnLiabsSerializer
from ratios.views import calculate_ratios
from wctl.views import wl_tl_assmt_calculations
from kfi.views import kfi_calculations
from ff.views import ff_calculations
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class GetAssetnLiabsView(APIView):
    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        years = company.years.all()
        for year in years:
            assetnliabscalculation(year.id)
        return Response(CompanyAssetnLiabsSerializer(years, many=True).data)


class UpdateAssetnLiabsView(APIView):
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
                return Response({'error': f'Year with id {company_data["id"]} does not exist'},
                                status=status.HTTP_404_NOT_FOUND)

            # Check if the token is authorized to update this company
            if year.company != company:
                return Response({'error': 'Unauthorized to update this company'}, status=status.HTTP_401_UNAUTHORIZED)

            # Retrieve the metrics data
            assetnliabs_data = company_data.get('metrics')
            if not assetnliabs_data:
                return Response({'error': 'Missing metrics data'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the opstmt instance associated with the company
            assetnliabs = year.assetnliabs

            # Deserialize and validate the opstmt data
            serializer = AssetnLiabsSerializer(assetnliabs, data=assetnliabs_data)
            if serializer.is_valid():
                serializer.save()
                calculate_ratios(year.id)
                wl_tl_assmt_calculations(year.id)
                kfi_calculations(year.id)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'success', 'companies': request.data}, status=status.HTTP_200_OK)




def assetnliabscalculation(year_id):
    year = Year.objects.get(id=year_id)
    opstmt = Opstmt.objects.get(year=year)
    asset_liab = AssetnLiabs.objects.get(year=year)
    ocacl = OcaOcl.objects.get(year=year)

    asset_liab.closingStockRM = opstmt.closing_stock_rm
    asset_liab.closingStockWIP = opstmt.closing_stock_wip
    asset_liab.closingStockFinishedGoods = opstmt.closing_stock_finished_goods
    asset_liab.otherNonCurrentAssets = ocacl.totalNonCurrentAssets
    asset_liab.totalNca = asset_liab.otherNonCurrentAssets + asset_liab.investmtLoanToAssociate
    asset_liab.otherLongTermLiab = ocacl.totalOtherTermLiabilities
    asset_liab.totalCurrentAssets = asset_liab.closingStockRM + asset_liab.closingStockWIP + asset_liab.closingStockFinishedGoods + asset_liab.consumableSpares + asset_liab.tradeDebtors6 + asset_liab.otherCurrentAssets
    asset_liab.save()


