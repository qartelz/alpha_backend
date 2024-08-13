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
    prev_year = Year.objects.get(id=pk - 1)
    opstmt = Opstmt.objects.get(year=cur_year)
    prev_opstmt = Opstmt.objects.get(year=prev_year)
    asst_and_liab = AssetnLiabs.objects.get(year=cur_year)
    prev_asst_and_liab = AssetnLiabs.objects.get(year=prev_year)
    oca_and_ocl = OcaOcl.objects.get(year=cur_year)
    prev_oca_and_ocl = OcaOcl.objects.get(year=prev_year)
    ratios = Ratios.objects.get(year=cur_year)
    prev_ratios = Ratios.objects.get(year=prev_year)
    wl_tl_assmt = WcTl.objects.get(year=cur_year)
    prev_wl_tl_assmt = WcTl.objects.get(year=prev_year)
    kfi = KFI.objects.get(year=cur_year)
    prev_kfi = KFI.objects.get(year=prev_year)
    ff = FF.objects.get(year=cur_year)


    if opstmt.pbd_it > 0:
        ff.net_profit_after_tax = opstmt.pbd_it
    else:
        ff.net_profit_after_tax = 0
    ff.depreciation = asst_and_liab.lessDepreciation - prev_asst_and_liab.lessDepreciation
    ff.increase_in_capital_reserves = (asst_and_liab.paidUpCapital + asst_and_liab.reservesSurplus) - (
            prev_asst_and_liab.paidUpCapital + prev_asst_and_liab.reservesSurplus)
    ff.increase_in_term_loan = ff.increase_in_term_loan_final
    if (asst_and_liab.otherLongTermLiab - prev_asst_and_liab.otherLongTermLiab) > 0:
        ff.increase_in_other_term_liabilities = asst_and_liab.otherLongTermLiab - prev_asst_and_liab.otherLongTermLiab
    else:
        ff.increase_in_other_term_liabilities = 0
    if (prev_asst_and_liab.grossBlock - asst_and_liab.grossBlock) > 0:
        ff.decrease_in_fixed_assets = prev_asst_and_liab.grossBlock - asst_and_liab.grossBlock
    else:
        ff.decrease_in_fixed_assets = 0
    if (prev_asst_and_liab.totalNca - asst_and_liab.totalNca) > 0:
        ff.decrease_in_non_current_assets = prev_asst_and_liab.totalNca - asst_and_liab.totalNca
    else:
        ff.decrease_in_non_current_assets = 0

    if (prev_asst_and_liab.totalIa - asst_and_liab.totalIa) > 0:
        ff.decrease_in_intangible_assets = prev_asst_and_liab.totalIa - asst_and_liab.totalIa
    else:
        ff.decrease_in_intangible_assets = 0

    ff.total_long_term_sources = ff.net_profit_after_tax + ff.depreciation + ff.increase_in_capital_reserves + ff.increase_in_term_loan + ff.increase_in_other_term_liabilities + ff.decrease_in_fixed_assets + ff.decrease_in_non_current_assets + ff.decrease_in_intangible_assets

    if opstmt.net_profit_after_tax_loss < 0:
        ff.net_loss = opstmt.net_profit_after_tax_loss * -1
    else:
        ff.net_loss = 0

    if (prev_asst_and_liab.grossBlock - asst_and_liab.grossBlock) < 0:
        ff.increase_in_fixed_assets = (prev_asst_and_liab.grossBlock - asst_and_liab.grossBlock) * -1
    else:
        ff.increase_in_fixed_assets = 0

    if (prev_asst_and_liab.totalNca - asst_and_liab.totalNca) < 0:
        ff.increase_in_non_current_assets = (prev_asst_and_liab.totalNca - asst_and_liab.totalNca) * -1
    else:
        ff.increase_in_non_current_assets = 0

    if (prev_asst_and_liab.totalIa - asst_and_liab.totalIa) < 0:
        ff.increase_intangible_assets = (prev_asst_and_liab.totalIa - asst_and_liab.totalIa) * -1
    else:
        ff.increase_intangible_assets = 0

    ff.decrease_in_term_loan = ff.decrease_in_term_loan_final
    if (asst_and_liab.otherLongTermLiab - prev_asst_and_liab.otherLongTermLiab) < 0:
        ff.decrease_in_otl = (asst_and_liab.otherLongTermLiab - prev_asst_and_liab.otherLongTermLiab) * -1
    else:
        ff.decrease_in_otl = 0
    ff.dividend_payments = opstmt.dividend_drawings
    ff.total_long_term_uses = ff.net_loss + ff.increase_in_fixed_assets + ff.increase_in_non_current_assets + ff.increase_intangible_assets + ff.decrease_in_term_loan + ff.decrease_in_otl + ff.dividend_payments
    ff.long_term_surplus_deficit = ff.total_long_term_sources - ff.total_long_term_uses
    ff.increase_decrease_in_ca = asst_and_liab.totalCurrentAssets - prev_asst_and_liab.totalCurrentAssets
    ff.inc_dec_in_cl_excl_bank_borrowing = (asst_and_liab.sundryCreditorsTrade + asst_and_liab.otherCurrentLiab) - (
            prev_asst_and_liab.sundryCreditorsTrade + prev_asst_and_liab.otherCurrentLiab)
    ff.increase_decrease_wc_gap = ff.increase_decrease_in_ca - ff.inc_dec_in_cl_excl_bank_borrowing
    ff.net_surplus_deficit = ff.long_term_surplus_deficit - ff.increase_decrease_wc_gap
    ff.inc_dec_in_bank_borrowing = (asst_and_liab.wcBorrowingsFromIob + asst_and_liab.wcFromBanksInstitution) - (
            prev_asst_and_liab.wcBorrowingsFromIob + prev_asst_and_liab.wcFromBanksInstitution)

    # Fund Flow Statement

    ff.long_term_sources = ff.total_long_term_sources
    ff.long_term_uses = ff.total_long_term_uses
    ff.surplus_deficit = ff.long_term_sources - ff.long_term_uses
    ff.long_term_uses_vs_sources = ff.long_term_uses / ff.long_term_sources

    # Building Up of NWC (Net Working Capital) - Sources

    if (kfi.bank_outstanding - prev_kfi.bank_outstanding) > 0:
        ff.increase_in_bank_borrowings = kfi.bank_outstanding - prev_kfi.bank_outstanding
    else:
        ff.increase_in_bank_borrowings = 0
    if (asst_and_liab.sundryCreditorsTrade - prev_asst_and_liab.sundryCreditorsTrade) > 0:
        ff.increase_in_sundry_creditors = asst_and_liab.sundryCreditorsTrade - prev_asst_and_liab.sundryCreditorsTrade
    else:
        ff.increase_in_sundry_creditors = 0
    if (asst_and_liab.otherCurrentLiab - prev_asst_and_liab.otherCurrentLiab) > 0:
        ff.increase_in_other_current_liabilities = asst_and_liab.otherCurrentLiab - prev_asst_and_liab.otherCurrentLiab
    else:
        ff.increase_in_other_current_liabilities = 0

    if (wl_tl_assmt.TOTAL_INVENTORY - prev_wl_tl_assmt.TOTAL_INVENTORY) < 0:
        ff.decrease_in_inventory = (wl_tl_assmt.TOTAL_INVENTORY - prev_wl_tl_assmt.TOTAL_INVENTORY) * -1
    else:
        ff.decrease_in_inventory = 0

    if (asst_and_liab.tradeDebtors6 - prev_asst_and_liab.tradeDebtors6) < 0:
        ff.decrease_in_receivables = (asst_and_liab.tradeDebtors6 - prev_asst_and_liab.tradeDebtors6) * -1
    else:
        ff.decrease_in_receivables = 0
    if (oca_and_ocl.totalOtherCurrentAssets - prev_oca_and_ocl.totalOtherCurrentAssets) < 0:
        ff.decrease_in_other_current_assets = (
                                                      oca_and_ocl.totalOtherCurrentAssets - prev_oca_and_ocl.totalOtherCurrentAssets) * -1
    else:
        ff.decrease_in_other_current_assets = 0
    ff.total_short_term_sources = ff.increase_in_bank_borrowings + ff.increase_in_sundry_creditors + ff.increase_in_other_current_liabilities + ff.decrease_in_inventory + ff.decrease_in_receivables + ff.decrease_in_other_current_assets

    # Building Up of NWC (Net Working Capital) - Uses

    if (kfi.bank_outstanding - prev_kfi.bank_outstanding) < 0:
        ff.decrease_in_bank_borrowings = (kfi.bank_outstanding - prev_kfi.bank_outstanding) * -1
    else:
        ff.decrease_in_bank_borrowings = 0
    if (asst_and_liab.sundryCreditorsTrade - prev_asst_and_liab.sundryCreditorsTrade) < 0:
        ff.decrease_in_sundry_creditors = (
                                                  asst_and_liab.sundryCreditorsTrade - prev_asst_and_liab.sundryCreditorsTrade) * -1
    else:
        ff.decrease_in_sundry_creditors = 0
    if (asst_and_liab.otherCurrentLiab - prev_asst_and_liab.otherCurrentLiab) < 0:
        ff.decrease_in_ocl = (asst_and_liab.otherCurrentLiab - prev_asst_and_liab.otherCurrentLiab) * -1
    else:
        ff.decrease_in_ocl = 0
    if (wl_tl_assmt.TOTAL_INVENTORY - prev_wl_tl_assmt.TOTAL_INVENTORY) > 0:
        ff.increase_in_inventory = (wl_tl_assmt.TOTAL_INVENTORY - prev_wl_tl_assmt.TOTAL_INVENTORY)
    else:
        ff.increase_in_inventory = 0
    if (asst_and_liab.tradeDebtors6 - prev_asst_and_liab.tradeDebtors6) > 0:
        ff.increase_in_receivables = (asst_and_liab.tradeDebtors6 - prev_asst_and_liab.tradeDebtors6)
    else:
        ff.increase_in_receivables = 0
    if (oca_and_ocl.totalOtherCurrentAssets - prev_oca_and_ocl.totalOtherCurrentAssets) > 0:
        ff.increase_in_oca = (oca_and_ocl.totalOtherCurrentAssets - prev_oca_and_ocl.totalOtherCurrentAssets)
    else:
        ff.increase_in_oca = 0
    ff.total_short_term_uses = ff.decrease_in_bank_borrowings + ff.decrease_in_sundry_creditors + ff.decrease_in_ocl + ff.increase_in_inventory + ff.increase_in_receivables + ff.increase_in_oca

    # NWC

    ff.nwc_beginning_year = prev_ratios.net_working_capital
    ff.increase_decrease_in_nwc = ratios.increase_and_decrease_fi
    ff.nwc_end_year = ff.nwc_beginning_year + ff.increase_decrease_in_nwc

    # Sources and Uses Totals

    ff.long_term_sources_total = ff.total_long_term_sources
    ff.short_term_sources_total = ff.total_short_term_sources
    ff.total_sources = ff.long_term_sources_total + ff.short_term_sources_total

    ff.long_term_uses_total = ff.total_long_term_uses
    ff.short_term_uses_total = ff.total_short_term_uses
    ff.total_uses = ff.long_term_uses_total + ff.short_term_uses_total

    # Final check

    ff.tallied_difference = ff.total_sources - ff.total_uses

    # Term Loan details

    ff.term_loan = asst_and_liab.termLoanIob + asst_and_liab.termLoanOtherBanks + asst_and_liab.termLoanInstitution
    # ff.increase_in_term_loan_final =
    # ff.decrease_in_term_loan_final =
