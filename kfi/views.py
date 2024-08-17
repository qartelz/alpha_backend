from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from wctl.models import WcTl
from .models import KFI
from ratios.models import Ratios
from assetnliabs.models import AssetnLiabs
from ocaocl.models import OcaOcl
from wctl.models import WcTl
from opstmt.models import Year, Company, Opstmt
from .serializers import KfiSerializer, CompanyKfiSerializer
from wctl.views import wl_tl_assmt_calculations
from ratios.views import calculate_ratios

# Create your views here.
class GetKFIView(APIView):
    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        years = company.years.all()
        for year in years:
            calculate_ratios(year.id)
            wl_tl_assmt_calculations(year.id)
            kfi_calculations(year.id)
        return Response(CompanyKfiSerializer(years, many=True).data)


# class UpdateKFIView(APIView):
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
#             kfi_data = company_data.get('metrics')
#             if not kfi_data:
#                 return Response({'error': 'Missing metrics data'}, status=status.HTTP_400_BAD_REQUEST)

#             # Retrieve the opstmt instance associated with the company
#             kfi = company.kfi

#             # Deserialize and validate the opstmt data
#             serializer = KfiSerializer(kfi, data=kfi_data)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'status': 'success', 'companies': request.data}, status=status.HTTP_200_OK)


def kfi_calculations(pk):
    year = Year.objects.get(id=pk)
    opstmt = Opstmt.objects.get(year=year)
    asst_and_liab = AssetnLiabs.objects.get(year=year)
    oca_and_ocl = OcaOcl.objects.get(year=year)
    ratios = Ratios.objects.get(year=year)
    wl_tl_assmt = WcTl.objects.get(year=year)
    kfi = KFI.objects.get(year=year)

    kfi.net_sales = ratios.NET_SALES_PROF_RATIOS
    kfi.percent_rise_fall_in_sales = ratios.percent_rise_ans_fall_in_sales
    kfi.operating_profit = opstmt.operating_profit_loss
    kfi.net_profit_after_tax = ratios.NET_PROFIT
    kfi.cash_accruals = opstmt.cash_accruals
    kfi.net_working_capital = ratios.net_working_capital
    kfi.current_ratio = ratios.current_ratio
    kfi.tnw = ratios.tangible_net_worth
    kfi.tnw_adjusted = ratios.TNW_Adjusted
    kfi.tol_tnw = ratios.TOl_and_TNW
    kfi.tol_tnw_adjusted = ratios.TOL_and_TNW_Adjusted
    kfi.tol_tnw_quasi_equity = ratios.TOL_and_TNW_Quasi_Equity
    kfi.funded_debt_tnw = ratios.Funded_Debt_and_TNW
    kfi.gross_fixed_asset_term_loan = wl_tl_assmt.Gross_Fixed_Assets_and_Term_Loan_O_and_s

    kfi.capital_and_reserves = asst_and_liab.netWorth
    kfi.long_term_liabilities = asst_and_liab.longTermLiab
    kfi.current_liabilities = asst_and_liab.totalCurrentLiab
    kfi.total_liabilities = asst_and_liab.totalLiab

    kfi.fixed_assets = asst_and_liab.netFixedAssets
    kfi.non_current_assets = asst_and_liab.totalNca
    kfi.current_assets = asst_and_liab.totalCurrentAssets
    kfi.intangible_assets = asst_and_liab.totalIa
    kfi.total_assets = asst_and_liab.totalAssets

    kfi.profit_loss_after_tax = opstmt.net_profit_after_tax_loss
    kfi.closing_balance = ratios.tangible_net_worth

    kfi.finished_goods = wl_tl_assmt.finished_goods
    kfi.months_cost_of_sales = wl_tl_assmt.months_cost_of_sales
    kfi.receivables = wl_tl_assmt.RECEIVABLES
    kfi.months_gross_sales = wl_tl_assmt.months_gross_sales
    kfi.trade_creditors = wl_tl_assmt.TRADE_CREDITORS
    kfi.months_purchases = wl_tl_assmt.months_purchases

    kfi.net_sales_NAYAK_COMMITTEE = ratios.net_sale
    kfi.twenty_five_percent_of_net_sales = kfi.net_sales_NAYAK_COMMITTEE * 0.25
    kfi.less_five_percent_margin = ratios.net_sale * 0.05
    kfi.eligible_bank_borrowings = kfi.twenty_five_percent_of_net_sales - kfi.less_five_percent_margin
    kfi.estimated_nwc_wc_margin = wl_tl_assmt.Actual_and_Projected_N_W_C
    kfi.nwc_shortfall = min((kfi.estimated_nwc_wc_margin - kfi.less_five_percent_margin), 0)

    kfi.stock_value = wl_tl_assmt.TOTAL_INVENTORY
    kfi.sundry_creditors = wl_tl_assmt.TRADE_CREDITORS
    kfi.paid_stock = kfi.stock_value - kfi.sundry_creditors
    kfi.margin_25_percent = kfi.paid_stock * 0.25
    if (kfi.paid_stock - kfi.margin_25_percent) < 1:
        kfi.drawing_power_1 = 0
    else:
        kfi.drawing_power_1 = kfi.paid_stock - kfi.margin_25_percent
    kfi.book_debts = wl_tl_assmt.RECEIVABLES
    kfi.margin_50_percent = kfi.book_debts * .50
    if (kfi.book_debts - kfi.margin_50_percent) < 1:
        kfi.drawing_power_2 = 0
    else:
        kfi.drawing_power_2 = kfi.book_debts - kfi.margin_50_percent
    kfi.total_eligible_limit = kfi.drawing_power_1 + kfi.drawing_power_2
    kfi.bank_outstanding = asst_and_liab.wcBorrowingsFromIob + asst_and_liab.wcFromBanksInstitution
    kfi.save()
