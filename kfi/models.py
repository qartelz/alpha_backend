from django.db import models
from opstmt.models import Company, Year

# Create your models here.
class KFI(models.Model):
    year = models.OneToOneField(Year, on_delete=models.CASCADE, related_name='kfi')
    net_sales = models.FloatField(default=0)
    percent_rise_fall_in_sales = models.FloatField(default=0)
    operating_profit = models.FloatField(default=0)
    net_profit_after_tax = models.FloatField(default=0)
    cash_accruals = models.FloatField(default=0)
    net_working_capital = models.FloatField(default=0)
    current_ratio = models.FloatField(default=0)
    tnw = models.FloatField(default=0)
    tnw_adjusted = models.FloatField(default=0)
    tol_tnw = models.FloatField(default=0)
    tol_tnw_adjusted = models.FloatField(default=0)
    tol_tnw_quasi_equity = models.FloatField(default=0)
    funded_debt_tnw = models.FloatField(default=0)
    gross_fixed_asset_term_loan = models.FloatField(default=0)

    #  ABRIDGED FINANCIAL LIABILITIES

    capital_and_reserves = models.FloatField(default=0)
    long_term_liabilities = models.FloatField(default=0)
    current_liabilities = models.FloatField(default=0)
    total_liabilities = models.FloatField(default=0)

    #  ABRIDGED FINANCIAL ASSETS

    fixed_assets = models.FloatField(default=0)
    non_current_assets = models.FloatField(default=0)
    current_assets = models.FloatField(default=0)
    intangible_assets = models.FloatField(default=0)
    total_assets = models.FloatField(default=0)

    #  MOVEMENT OF TNW

    opening_balance = models.FloatField(default=0)
    profit_loss_after_tax = models.FloatField(default=0)
    increase_in_capital = models.FloatField(default=0)
    drawings = models.FloatField(default=0)
    closing_balance = models.FloatField(default=0)

    #  INVENTORY HOLDINGS

    finished_goods = models.FloatField(default=0)
    months_cost_of_sales = models.FloatField(default=0)
    receivables = models.FloatField(default=0)
    months_gross_sales = models.FloatField(default=0)
    trade_creditors = models.FloatField(default=0)
    months_purchases = models.FloatField(default=0)

    #  NAYAK COMMITTEE

    net_sales_NAYAK_COMMITTEE = models.FloatField(default=0, verbose_name='Net Sales')
    twenty_five_percent_of_net_sales = models.FloatField(default=0, verbose_name='25% of Net Sales')
    less_five_percent_margin = models.FloatField(default=0, verbose_name='Less 5% Margin')
    eligible_bank_borrowings = models.FloatField(default=0, verbose_name='Eligible Bank Borrowings')
    estimated_nwc_wc_margin = models.FloatField(default=0, verbose_name='Estimated NWC (WC Margin)')
    nwc_shortfall = models.FloatField(default=0, verbose_name='NWC Shortfall')

    #  STRUCTURE OF LIMITS

    stock_value = models.FloatField(default=0, verbose_name='Stock Value')
    sundry_creditors = models.FloatField(default=0, verbose_name='Sundry Creditors')
    paid_stock = models.FloatField(default=0, verbose_name='Paid Stock')
    margin_25_percent = models.FloatField(default=0, verbose_name='Margin 25%')
    drawing_power_1 = models.FloatField(default=0, verbose_name='Drawing Power 1')
    book_debts = models.FloatField(default=0, verbose_name='Book Debts')
    margin_50_percent = models.FloatField(default=0, verbose_name='Margin 50%')
    drawing_power_2 = models.FloatField(default=0, verbose_name='Drawing Power 2')
    total_eligible_limit = models.FloatField(default=0, verbose_name='Total Eligible Limit')
    bank_outstanding = models.FloatField(default=0, verbose_name='Bank Outstanding')
