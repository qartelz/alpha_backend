from django.db import models
from opstmt.models import Year, Company


class FF(models.Model):
    year = models.OneToOneField(Year, on_delete=models.CASCADE, related_name='ff')

    # Sources
    net_profit_after_tax = models.FloatField(default=0.0)
    depreciation = models.FloatField(default=0.0)
    increase_in_capital_reserves = models.FloatField(default=0.0)
    increase_in_term_loan = models.FloatField(default=0.0)
    increase_in_other_term_liabilities = models.FloatField(default=0.0)
    decrease_in_fixed_assets = models.FloatField(default=0.0)
    decrease_in_non_current_assets = models.FloatField(default=0.0)
    decrease_in_intangible_assets = models.FloatField(default=0.0)
    total_long_term_sources = models.FloatField(default=0.0)

    # Uses
    net_loss = models.FloatField(default=0.0)
    increase_in_fixed_assets = models.FloatField(default=0.0)
    increase_in_non_current_assets = models.FloatField(default=0.0)
    increase_intangible_assets = models.FloatField(default=0.0)
    decrease_in_term_loan = models.FloatField(default=0.0)
    decrease_in_otl = models.FloatField(default=0.0)
    dividend_payments = models.FloatField(default=0.0)
    total_long_term_uses = models.FloatField(default=0.0)
    long_term_surplus_deficit = models.FloatField(default=0.0)
    increase_decrease_in_ca = models.FloatField(default=0.0)
    inc_dec_in_cl_excl_bank_borrowing = models.FloatField(default=0.0)
    increase_decrease_wc_gap = models.FloatField(default=0.0)
    net_surplus_deficit = models.FloatField(default=0.0)
    inc_dec_in_bank_borrowing = models.FloatField(default=0.0)

    # Fund Flow Statement
    long_term_sources = models.FloatField(default=0.0)
    long_term_uses = models.FloatField(default=0.0)
    surplus_deficit = models.FloatField(default=0.0)
    long_term_uses_vs_sources = models.FloatField(default=0.0)

    # Building Up of NWC (Net Working Capital) - Sources
    increase_in_bank_borrowings = models.FloatField(default=0.0)
    increase_in_sundry_creditors = models.FloatField(default=0.0)
    increase_in_other_current_liabilities = models.FloatField(default=0.0)
    decrease_in_inventory = models.FloatField(default=0.0)
    decrease_in_receivables = models.FloatField(default=0.0)
    decrease_in_other_current_assets = models.FloatField(default=0.0)
    total_short_term_sources = models.FloatField(default=0.0)

    # Building Up of NWC (Net Working Capital) - Uses
    decrease_in_bank_borrowings = models.FloatField(default=0.0)
    decrease_in_sundry_creditors = models.FloatField(default=0.0)
    decrease_in_ocl = models.FloatField(default=0.0)
    increase_in_inventory = models.FloatField(default=0.0)
    increase_in_receivables = models.FloatField(default=0.0)
    increase_in_oca = models.FloatField(default=0.0)
    total_short_term_uses = models.FloatField(default=0.0)

    # NWC
    nwc_beginning_year = models.FloatField(default=0.0)
    increase_decrease_in_nwc = models.FloatField(default=0.0)
    nwc_end_year = models.FloatField(default=0.0)

    # Sources and Uses Totals
    long_term_sources_total = models.FloatField(default=0.0)
    short_term_sources_total = models.FloatField(default=0.0)
    total_sources = models.FloatField(default=0.0)

    long_term_uses_total = models.FloatField(default=0.0)
    short_term_uses_total = models.FloatField(default=0.0)
    total_uses = models.FloatField(default=0.0)

    # Final check
    tallied_difference = models.FloatField(default=0.0)

    # Term Loan details
    term_loan = models.FloatField(default=0.0)
    increase_in_term_loan_final = models.FloatField(default=0.0)
    decrease_in_term_loan_final = models.FloatField(default=0.0)
