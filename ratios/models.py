from django.db import models
from opstmt.models import Year

class Ratios(models.Model):
    year = models.OneToOneField(Year, on_delete=models.CASCADE, related_name='ratios')
    net_sale = models.FloatField(default=0)
    consumption_of_raw_materials = models.FloatField(default=0)
    cost_of_production = models.FloatField(default=0)
    cost_of_sales = models.FloatField(default=0)
    production_at_sale_value = models.FloatField(default=0)
    cost_of_production_Depn_and_Sales_in_FG = models.FloatField(default=0)
    cost_of_sales_Depn_and_Sales = models.FloatField(default=0)
    R_M_and_production_Sales_percent = models.FloatField(default=0)
    Net_Profit_and_Sales_percent = models.FloatField(default=0)
    Operaing_Cost_and_Cost_of_Sales_percent = models.FloatField(default=0)
    Mfg_Exp_and_Cost_of_Sales_percent = models.FloatField(default=0)
    Selling_and_Admn_Exp_and_Cost_of_Sales_percent = models.FloatField(default=0)
    Fin_Charges_and_Cost_of_Sales_percent = models.FloatField(default=0)

    # FINANCIAL INDICATORS

    tangible_net_worth = models.FloatField(default=0)
    increase_and_decrease = models.FloatField(default=0)
    TNW_Adjusted = models.FloatField(default=0)
    TNW_Quasi_Equity = models.FloatField(default=0)
    net_working_capital = models.FloatField(default=0)
    increase_and_decrease_fi = models.FloatField(default=0)
    current_ratio = models.FloatField(default=0)
    TOl_and_TNW = models.FloatField(default=0)
    TOL_and_TNW_Quasi_Equity = models.FloatField(default=0)
    TOL_and_TNW_Adjusted = models.FloatField(default=0)
    Funded_Debt_and_TNW = models.FloatField(default=0)

    # PROFITABILITY RATIOS:

    NET_SALES_PROF_RATIOS = models.FloatField(default=0)
    percent_rise_ans_fall_in_sales = models.FloatField(default=0)
    operating_profit = models.FloatField(default=0)
    PBDIT = models.FloatField(default=0)
    NET_PROFIT = models.FloatField(default=0)
    Depreciation = models.FloatField(default=0)
    cash_accruals = models.FloatField(default=0)
    PBDIT_and_Sales_percent = models.FloatField(default=0)
    operating_cost_and_sales_percent = models.FloatField(default=0)
    Net_Profit_and_Sales_percent_PROF_RATIOS = models.FloatField(default=0)
    Net_Profit_and_TNW_percent = models.FloatField(default=0)
    sales_and_TNW = models.FloatField(default=0)

    # BANK FINANCE :
    total_bank_borrowings = models.FloatField(default=0)
    Inc_and_dec_in_Bank_Borrowings_percent = models.FloatField(default=0)
    Bank_Finance_and_Current_Assets = models.FloatField(default=0)
    Inv_plus_Receivables_and_Sales_days = models.FloatField(default=0)
    PBDIT_and_Interest = models.FloatField(default=0)
