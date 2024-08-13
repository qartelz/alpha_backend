from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ratios
from assetnliabs.models import AssetnLiabs
from ocaocl.models import OcaOcl
from wctl.models import WcTl
from opstmt.models import Year, Company, Opstmt
from .serializers import RatiosSerializer, CompanyRatiosSerializer


# from rest_framework.permissions import IsA
# uthenticated

# Create your views here.
class GetRatiosView(APIView):
    def get(self, request, token_id):
        company = Company.objects.get(id=token_id)
        years = company.years.all()
        for year in years:
            calculate_ratios(year.id)
        return Response(CompanyRatiosSerializer(years, many=True).data)


# class UpdateRatiosView(APIView):
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
#             ratios_data = company_data.get('metrics')
#             if not ratios_data:
#                 return Response({'error': 'Missing metrics data'}, status=status.HTTP_400_BAD_REQUEST)

#             # Retrieve the opstmt instance associated with the company
#             ratios = company.ratios

#             # Deserialize and validate the opstmt data
#             serializer = RatiosSerializer(ratios, data=ratios_data)
#             if serializer.is_valid():
#                 serializer.save()
#                 print(f'ocaocl for {company.name} updated')
#             else:
#                 print(serializer.errors)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'status': 'success', 'companies': request.data}, status=status.HTTP_200_OK)


# Ratios Calculations
def calculate_ratios(pk):
    year = Year.objects.get(id=pk)
    opstmt = Opstmt.objects.get(year=year)
    asst_and_liab = AssetnLiabs.objects.get(year=year)
    oca_and_ocl = OcaOcl.objects.get(year=year)
    ratios = Ratios.objects.get(year=year)

    ratios.net_sale = opstmt.total_sales
    ratios.consumption_of_raw_materials = (opstmt.opening_stock_rm + opstmt.purchase_rm) - opstmt.closing_stock_rm
    ratios.cost_of_production = opstmt.cost_of_production
    ratios.cost_of_sales = opstmt.cost_of_sales
    ratios.production_at_sale_value = (
                                                  opstmt.total_sales + opstmt.closing_stock_finished_goods + opstmt.closing_stock_wip) - (
                                                  opstmt.opening_stock_finished_goods + opstmt.opening_stock_wip)
    if (
            ratios.production_at_sale_value + opstmt.closing_stock_finished_goods - opstmt.opening_stock_finished_goods) != 0:
        ratios.cost_of_production_Depn_and_Sales_in_FG = ((ratios.cost_of_production - ratios.Depreciation) / (
                    ratios.production_at_sale_value + opstmt.closing_stock_finished_goods - opstmt.opening_stock_finished_goods)) * 100
    else:
        ratios.cost_of_production_Depn_and_Sales_in_FG = 0
    if ratios.net_sale != 0:
        ratios.cost_of_sales_Depn_and_Sales = ((ratios.cost_of_sales - ratios.Depreciation) / ratios.net_sale) * 100
    else:
        ratios.cost_of_sales_Depn_and_Sales = 0
    if ratios.production_at_sale_value != 0:
        ratios.R_M_and_production_Sales_percent = (
                                                              ratios.consumption_of_raw_materials / ratios.production_at_sale_value) * 100
    else:
        ratios.R_M_and_production_Sales_percent = 0
    if opstmt.total_sales != 0:
        ratios.Net_Profit_and_Sales_percent = (opstmt.net_profit_after_tax_loss / opstmt.total_sales) * 100
    else:
        ratios.Net_Profit_and_Sales_percent = 0
    if opstmt.cost_of_sales != 0:
        ratios.Operaing_Cost_and_Cost_of_Sales_percent = (100 - (
                    opstmt.operating_profit_loss / opstmt.cost_of_sales)) * 100
    else:
        ratios.Operaing_Cost_and_Cost_of_Sales_percent = 0
    if opstmt.cost_of_sales != 0:
        ratios.Mfg_Exp_and_Cost_of_Sales_percent = (opstmt.mfg_direct_expenses / opstmt.cost_of_sales) * 100
    else:
        ratios.Mfg_Exp_and_Cost_of_Sales_percent = 0
    if opstmt.cost_of_sales != 0:
        ratios.Selling_and_Admn_Exp_and_Cost_of_Sales_percent = (
                                                                            opstmt.selling_adm_expenses / opstmt.cost_of_sales) * 100
    else:
        ratios.Selling_and_Admn_Exp_and_Cost_of_Sales_percent = 0

    if opstmt.cost_of_sales != 0:
        ratios.Fin_Charges_and_Cost_of_Sales_percent = (opstmt.interest_fin_charges / opstmt.cost_of_sales) * 100
    else:
        ratios.Fin_Charges_and_Cost_of_Sales_percent = 0
    ratios.tangible_net_worth = asst_and_liab.netWorth - asst_and_liab.totalIa
    ratios.TNW_Adjusted = ratios.tangible_net_worth - asst_and_liab.investmtLoanToAssociate
    ratios.TNW_Quasi_Equity = oca_and_ocl.unsecuredLoanPromotors + ratios.tangible_net_worth
    ratios.net_working_capital = asst_and_liab.totalCurrentAssets - asst_and_liab.totalCurrentLiab
    if asst_and_liab.totalCurrentLiab != 0:
        ratios.current_ratio = asst_and_liab.totalCurrentAssets / asst_and_liab.totalCurrentLiab
    else:
        ratios.current_ratio = 0
    if ratios.tangible_net_worth != 0:
        ratios.TOl_and_TNW = ((
                                          asst_and_liab.totalCurrentLiab + asst_and_liab.longTermLiab) - oca_and_ocl.revaluationReserve) / ratios.tangible_net_worth
    else:
        ratios.TOl_and_TNW = 0
    if (oca_and_ocl.unsecuredLoanPromotors + ratios.tangible_net_worth) != 0:

        ratios.TOL_and_TNW_Quasi_Equity = (asst_and_liab.totalOutsideLiab - oca_and_ocl.revaluationReserve) / (
                    oca_and_ocl.unsecuredLoanPromotors + ratios.tangible_net_worth)
    else:
        ratios.TOL_and_TNW_Quasi_Equity = 0

    # ratios.TOL_and_TNW_Adjusted = ((asst_and_liab.termLoanIob + asst_and_liab.capital_and_surplus) - oca_and_ocl.)/ratios.TNW_Adjusted
    if ratios.tangible_net_worth != 0:
        ratios.Funded_Debt_and_TNW = ((
                                                  asst_and_liab.longTermLiab + oca_and_ocl.otherTermLiabilities + oca_and_ocl.tlInstDueIn1YearBankInst) - (
                                                  oca_and_ocl.unsecuredLoanPromotors + oca_and_ocl.revaluationReserve)) / ratios.tangible_net_worth
    else:
        ratios.Funded_Debt_and_TNW = 0

    ratios.NET_SALES_PROF_RATIOS = opstmt.total_sales
    ratios.operating_profit = opstmt.operating_profit_loss
    ratios.PBDIT = opstmt.pbd_it
    ratios.NET_PROFIT = opstmt.net_profit_after_tax_loss
    ratios.Depreciation = opstmt.depreciation
    ratios.cash_accruals = opstmt.net_cash_accrual
    if ratios.NET_SALES_PROF_RATIOS != 0:
        ratios.PBDIT_and_Sales_percent = (ratios.PBDIT / ratios.NET_SALES_PROF_RATIOS) * 100
    else:
        ratios.PBDIT_and_Sales_percent = 0
    if opstmt.total_sales != 0:
        ratios.operating_cost_and_sales_percent = (opstmt.operating_profit_loss / opstmt.total_sales) * 100
    else:
        ratios.operating_cost_and_sales_percent = 0
    if opstmt.total_sales != 0:
        ratios.Net_Profit_and_Sales_percent_PROF_RATIOS = (opstmt.net_profit_after_tax_loss / opstmt.total_sales) * 100
    else:
        ratios.Net_Profit_and_Sales_percent_PROF_RATIOS = 0
    if ratios.tangible_net_worth != 0:
        ratios.Net_Profit_and_TNW_percent = (opstmt.net_profit_after_tax_loss / ratios.tangible_net_worth) * 100
    else:
        ratios.Net_Profit_and_TNW_percent = 0

    if ratios.tangible_net_worth != 0:
        ratios.sales_and_TNW = ratios.NET_SALES_PROF_RATIOS / ratios.tangible_net_worth
    else:
        ratios.sales_and_TNW = 0
    ratios.total_bank_borrowings = asst_and_liab.wcBorrowingsFromIob + asst_and_liab.wcFromBanksInstitution
    if asst_and_liab.totalCurrentAssets != 0:
        ratios.Bank_Finance_and_Current_Assets = (ratios.total_bank_borrowings / asst_and_liab.totalCurrentAssets) * 100
    else:
        ratios.Bank_Finance_and_Current_Assets = 0
    if ratios.net_sale != 0:
        ratios.Inv_plus_Receivables_and_Sales_days = ((
                                                                  asst_and_liab.closingStockRM + asst_and_liab.closingStockWIP + asst_and_liab.closingStockFinishedGoods + asst_and_liab.consumableSpares + asst_and_liab.tradeDebtors6) * 365) / ratios.net_sale
    else:
        ratios.Inv_plus_Receivables_and_Sales_days = 0
    if opstmt.interest_fin_charges != 0:
        ratios.PBDIT_and_Interest = ratios.PBDIT / opstmt.interest_fin_charges
    else:
        ratios.PBDIT_and_Interest = 0

    ratios.save()
