from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from wctl.models import WcTl
from .models import FF
from kfi.models import KFI
from ratios.models import Ratios
from assetnliabs.models import AssetnLiabs
from ocaocl.models import OcaOcl
from wctl.models import WcTl
from opstmt.models import Year, Company, Opstmt
from .serializers import FFSerializer, CompanyFFSerializer


# from rest_framework.permissions import IsAuthenticated

# Create your views here.
class GetFFView(APIView):
    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        years = company.years.all()
        # for year in years:
        #     kfi_calculations(year.id)
        return Response(CompanyFFSerializer(years, many=True).data)


def ff_calculations(pk):
    cur_year = Year.objects.get(id=pk)
    prev_year = Year.objects.get(id=pk-1)
    opstmt = Opstmt.objects.get(year=cur_year)
    prev_opstmt = Opstmt.objects.get(year=prev_year)
    asst_and_liab = AssetnLiabs.objects.get(year=cur_year)
    prev_asst_and_liab = AssetnLiabs.objects.get(year=prev_year)
    oca_and_ocl = OcaOcl.objects.get(year=cur_year)
    oca_and_ocl = OcaOcl.objects.get(year=prev_year)
    ratios = Ratios.objects.get(year=cur_year)
    wl_tl_assmt = WcTl.objects.get(year=cur_year)
    wl_tl_assmt = WcTl.objects.get(year=prev_year)
    kfi = KFI.objects.get(year=cur_year)
    kfi = KFI.objects.get(year=prev_year)
    ff = FF.objects.get(year=cur_year)

