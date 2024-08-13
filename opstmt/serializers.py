from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Company, Opstmt, Year

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['student','id']

class OpstmtSerializer(serializers.ModelSerializer):
    netSales = serializers.FloatField(source='net_sales', required=False, default=0)
    salesDomestic = serializers.FloatField(source='sales_domestic', required=False, default=0)
    salesExports = serializers.FloatField(source='sales_exports', required=False, default=0)
    others = serializers.FloatField(required=False, default=0)
    totalSales = serializers.FloatField(source='total_sales', required=False, default=0)
    openingStockFinishedGoods = serializers.FloatField(source='opening_stock_finished_goods', required=False, default=0)
    openingStockWIP = serializers.FloatField(source='opening_stock_wip', required=False, default=0)
    openingStockRM = serializers.FloatField(source='opening_stock_rm', required=False, default=0)
    purchaseRM = serializers.FloatField(source='purchase_rm', required=False, default=0)
    powerFuel = serializers.FloatField(source='power_fuel', required=False, default=0)
    directLabour = serializers.FloatField(source='direct_labour', required=False, default=0)
    repairsMaintenance = serializers.FloatField(source='repairs_maintenance', required=False, default=0)
    mfgDirectExpenses = serializers.FloatField(source='mfg_direct_expenses', required=False, default=0)
    depreciation = serializers.FloatField(required=False, default=0)
    closingStockFinishedGoods = serializers.FloatField(source='closing_stock_finished_goods', required=False, default=0)
    closingStockWIP = serializers.FloatField(source='closing_stock_wip', required=False, default=0)
    closingStockRM = serializers.FloatField(source='closing_stock_rm', required=False, default=0)
    costOfSales = serializers.FloatField(source='cost_of_sales', required=False, default=0)
    costOfProduction = serializers.FloatField(source='cost_of_production', required=False, default=0)
    grossProfitLoss = serializers.FloatField(source='gross_profit_loss', required=False, default=0)
    sellingAdmExpenses = serializers.FloatField(source='selling_adm_expenses', required=False, default=0)
    interestFinCharges = serializers.FloatField(source='interest_fin_charges', required=False, default=0)
    operatingProfitLoss = serializers.FloatField(source='operating_profit_loss', required=False, default=0)
    otherIncomeExpenses = serializers.FloatField(source='other_income_expenses', required=False, default=0)
    addOtherIncome = serializers.FloatField(source='add_other_income', required=False, default=0)
    lessOtherExpenses = serializers.FloatField(source='less_other_expenses', required=False, default=0)
    profitBeforeTax = serializers.FloatField(source='profit_before_tax', required=False, default=0)
    provisionForTaxes = serializers.FloatField(source='provision_for_taxes', required=False, default=0)
    netProfitAfterTaxLoss = serializers.FloatField(source='net_profit_after_tax_loss', required=False, default=0)
    pbdIT = serializers.FloatField(source='pbd_it', required=False, default=0)
    cashAccruals = serializers.FloatField(source='cash_accruals', required=False, default=0)
    dividendDrawings = serializers.FloatField(source='dividend_drawings', required=False, default=0)
    retainedProfit = serializers.FloatField(source='retained_profit', required=False, default=0)
    netCashAccrual = serializers.FloatField(source='net_cash_accrual', required=False, default=0)

    class Meta:
        model = Opstmt
        fields = [
            'netSales', 'salesDomestic', 'salesExports', 'others', 'totalSales', 
            'openingStockFinishedGoods', 'openingStockWIP', 'openingStockRM', 'purchaseRM', 
            'powerFuel', 'directLabour', 'repairsMaintenance', 'mfgDirectExpenses', 'depreciation', 
            'closingStockFinishedGoods', 'closingStockWIP', 'closingStockRM', 'costOfProduction', 'costOfSales',
            'grossProfitLoss', 'sellingAdmExpenses', 'interestFinCharges', 'operatingProfitLoss', 
            'otherIncomeExpenses', 'addOtherIncome', 'lessOtherExpenses', 'profitBeforeTax', 
            'provisionForTaxes', 'netProfitAfterTaxLoss', 'pbdIT', 'cashAccruals', 
            'dividendDrawings', 'retainedProfit', 'netCashAccrual'
        ]


class CompanyOpstmtSerializer(serializers.ModelSerializer):
    metrics = OpstmtSerializer(source='opstmt')  # Set read_only to True

    class Meta:
        model = Year
        fields = ['id','year', 'metrics']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials") 