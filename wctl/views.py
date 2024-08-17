from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import WcTl
from ratios.models import Ratios
from assetnliabs.models import AssetnLiabs
from ocaocl.models import OcaOcl
from wctl.models import WcTl
from opstmt.models import Year, Company, Opstmt
from .serializers import WctlSerializer, CompanyWcTlSerializer
from ratios.views import calculate_ratios

# from rest_framework.permissions import IsAuthenticated
# Create your views here.
class GetWcTlView(APIView):
    def get(self, request, token_id):
        company = Company.objects.get(id=token_id)
        years = company.years.all()
        for year in years:
            calculate_ratios(year.id)
            wl_tl_assmt_calculations(year.id)
        return Response(CompanyWcTlSerializer(years, many=True).data)


# class UpdateWcTlView(APIView):
#     def post(self, request, token_id):
#         try:
#             token = Token.objects.get(id=token_id)
#         except Token.DoesNotExist:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

#         companies_data = request.data

#         for company_data in companies_data:
#             # Retrieve the company instance
#             try:
#                 company = Company.objects.get(id=company_data['id'])
#             except Company.DoesNotExist:
#                 return Response({'error': f'Company with id {company_data["id"]} does not exist'},
#                                 status=status.HTTP_404_NOT_FOUND)

#             # Check if the token is authorized to update this company
#             if company.token != token:
#                 return Response({'error': 'Unauthorized to update this company'}, status=status.HTTP_401_UNAUTHORIZED)

#             # Retrieve the metrics data
#             wctl_data = company_data.get('metrics')
#             if not wctl_data:
#                 return Response({'error': 'Missing metrics data'}, status=status.HTTP_400_BAD_REQUEST)

#             # Retrieve the opstmt instance associated with the company
#             wctl = company.wctl

#             # Deserialize and validate the opstmt data
#             serializer = WctlSerializer(wctl, data=wctl_data)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'status': 'success', 'companies': request.data}, status=status.HTTP_200_OK)


def wl_tl_assmt_calculations(year_id):
    year = Year.objects.get(id=year_id)
    opstmt = Opstmt.objects.get(year=year)
    asst_and_liab = AssetnLiabs.objects.get(year=year)
    oca_and_ocl = OcaOcl.objects.get(year=year)
    ratios = Ratios.objects.get(year=year)
    wl_tl_assmt = WcTl.objects.get(year=year)

    wl_tl_assmt.Raw_Materials = asst_and_liab.closingStockRM
    if opstmt.purchase_rm != 0:
        wl_tl_assmt.months_consumption = (asst_and_liab.closingStockRM / opstmt.purchase_rm) * 12
    else:
        wl_tl_assmt.months_consumption = 0

    wl_tl_assmt.stock_in_process = asst_and_liab.closingStockWIP
    if opstmt.cost_of_sales != 0:
        wl_tl_assmt.months_cost_of_production = (asst_and_liab.closingStockWIP / opstmt.cost_of_sales) * 12
    else:
        wl_tl_assmt.months_cost_of_production = 0

    wl_tl_assmt.finished_goods = asst_and_liab.closingStockFinishedGoods
    if opstmt.cost_of_sales != 0:
        wl_tl_assmt.months_cost_of_sales = (asst_and_liab.closingStockFinishedGoods / opstmt.cost_of_sales) * 12
    else:
        wl_tl_assmt.months_cost_of_sales = 0

    wl_tl_assmt.other_consumable_spares = asst_and_liab.consumableSpares
    if opstmt.repairs_maintenance != 0:
        wl_tl_assmt.months_consumption_cs = (asst_and_liab.consumableSpares / opstmt.repairs_maintenance) * 12
    else:
        wl_tl_assmt.months_consumption_cs = 0

    wl_tl_assmt.TOTAL_INVENTORY = wl_tl_assmt.Raw_Materials + wl_tl_assmt.stock_in_process + wl_tl_assmt.finished_goods + wl_tl_assmt.other_consumable_spares
    wl_tl_assmt.RECEIVABLES = oca_and_ocl.sundryDebtorsGreater6months + asst_and_liab.tradeDebtors6
    if opstmt.total_sales != 0:
        wl_tl_assmt.months_gross_sales = (wl_tl_assmt.RECEIVABLES / opstmt.total_sales) * 12
    else:
        wl_tl_assmt.months_gross_sales = 0

    wl_tl_assmt.other_current_assets = oca_and_ocl.totalOtherCurrentAssets
    wl_tl_assmt.TOTAL_CHARGEABLE_CA = wl_tl_assmt.TOTAL_INVENTORY + wl_tl_assmt.RECEIVABLES + wl_tl_assmt.other_current_assets
    wl_tl_assmt.TRADE_CREDITORS = asst_and_liab.sundryCreditorsTrade
    if opstmt.purchase_rm != 0:
        wl_tl_assmt.months_purchases = (asst_and_liab.sundryCreditorsTrade / opstmt.purchase_rm) * 12
    else:
        wl_tl_assmt.months_purchases = 0
    wl_tl_assmt.other_current_liabilities = oca_and_ocl.totalOtherCurrentLiabilities
    wl_tl_assmt.TOTAL_LIABILITIES = wl_tl_assmt.TRADE_CREDITORS + wl_tl_assmt.other_current_liabilities
    wl_tl_assmt.Working_Capital_Gap_A = wl_tl_assmt.TOTAL_CHARGEABLE_CA - wl_tl_assmt.TOTAL_LIABILITIES
    wl_tl_assmt.twenrtfive_percent_Margin_on_C_A_B = wl_tl_assmt.TOTAL_CHARGEABLE_CA * 0.25
    wl_tl_assmt.Actual_and_Projected_N_W_C = ratios.net_working_capital
    wl_tl_assmt.A_B_I = wl_tl_assmt.Working_Capital_Gap_A - wl_tl_assmt.twenrtfive_percent_Margin_on_C_A_B
    wl_tl_assmt.A_C_II = wl_tl_assmt.Working_Capital_Gap_A - wl_tl_assmt.Actual_and_Projected_N_W_C
    wl_tl_assmt.MPBF_Lower_of_I_or_II = min(
        (wl_tl_assmt.Working_Capital_Gap_A - wl_tl_assmt.twenrtfive_percent_Margin_on_C_A_B),
        (wl_tl_assmt.Working_Capital_Gap_A - wl_tl_assmt.Actual_and_Projected_N_W_C))
    wl_tl_assmt.Shortfall_in_NWC = min(
        (wl_tl_assmt.Actual_and_Projected_N_W_C - wl_tl_assmt.twenrtfive_percent_Margin_on_C_A_B), 0)
    wl_tl_assmt.Gross_Fixed_Assets = asst_and_liab.grossBlock
    wl_tl_assmt.WDV_of_Fixed_Assets = asst_and_liab.netFixedAssets
    wl_tl_assmt.Term_Loan_O_and_s = asst_and_liab.termLoanIob + asst_and_liab.termLoanInstitution + wl_tl_assmt.TL_Installment

    if wl_tl_assmt.Term_Loan_O_and_s != 0:
        wl_tl_assmt.Gross_Fixed_Assets_and_Term_Loan_O_and_s = wl_tl_assmt.Gross_Fixed_Assets / wl_tl_assmt.Term_Loan_O_and_s
    else:
        wl_tl_assmt.Gross_Fixed_Assets_and_Term_Loan_O_and_s = 0

    wl_tl_assmt.Margin = wl_tl_assmt.WDV_of_Fixed_Assets - wl_tl_assmt.Term_Loan_O_and_s
    if wl_tl_assmt.Margin < 1 and wl_tl_assmt.WDV_of_Fixed_Assets != 0:
        wl_tl_assmt.Security_Margin = (wl_tl_assmt.Margin / wl_tl_assmt.WDV_of_Fixed_Assets) * 100
    else:
        wl_tl_assmt.Security_Margin = 0
    if wl_tl_assmt.Term_Loan_O_and_s != 0:
        wl_tl_assmt.Fixed_Asset_Coverage_Ratio = wl_tl_assmt.WDV_of_Fixed_Assets / wl_tl_assmt.Term_Loan_O_and_s
    else:
        wl_tl_assmt.Fixed_Asset_Coverage_Ratio = 0

    # if wl_tl_assmt.Difference > 0:
    #     wl_tl_assmt.IF_Cash_accrual_TL_Installment = "Yes"
    # else:
    #     wl_tl_assmt.IF_Cash_accrual_TL_Installment = "No"

    wl_tl_assmt.Cash_Accrual = opstmt.net_cash_accrual
    wl_tl_assmt.TL_Installment = oca_and_ocl.otherTermLiabilities + oca_and_ocl.tlInstDueIn1YearBankInst
    wl_tl_assmt.Difference = round((wl_tl_assmt.Cash_Accrual - wl_tl_assmt.TL_Installment), 2)
    wl_tl_assmt.save()
