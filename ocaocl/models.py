from django.db import models
from opstmt.models import Year

# Create your models here.
class OcaOcl(models.Model):
    year = models.OneToOneField(Year, on_delete=models.CASCADE, related_name='ocaocl')

    # Fields for Other Current Assets
    cashAndBankBalance = models.FloatField(default=0)
    fixedDepositsWithBank = models.FloatField(default=0)
    advanceIncomeTaxSalesTax = models.FloatField(default=0)
    advanceToStaffDirectors = models.FloatField(default=0)
    advanceToSuppliers = models.FloatField(default=0)
    exciseCustomsTuf = models.FloatField(default=0)
    loansAndAdvances = models.FloatField(default=0)
    others = models.FloatField(default=0)
    totalOtherCurrentAssets = models.FloatField(default=0)

    # Fields for Non-Current Assets
    securityDepositsEbEtc = models.FloatField(default=0)
    loanAndAdvances = models.FloatField(default=0)
    sundryDebtorsGreater6months = models.FloatField(default=0)
    investment = models.FloatField(default=0)
    interestAccruedOnLoans = models.FloatField(default=0)
    othersNonCurrent = models.FloatField(default=0)
    totalNonCurrentAssets = models.FloatField(default=0)

    # Fields for Other Current Liabilities
    tlInstDueIn1YearIob = models.FloatField(default=0)
    tlInstDueIn1YearBankInst = models.FloatField(default=0)
    sundryCreditorsExpenses = models.FloatField(default=0)
    expensesPayable = models.FloatField(default=0)
    provisionForTaxEtc = models.FloatField(default=0)
    othersCurrentLiabilities = models.FloatField(default=0)
    totalOtherCurrentLiabilities = models.FloatField(default=0)

    # Fields for Other Term Liabilities
    otherTermLiabilities = models.FloatField(default=0)
    unsecuredLoanPromotors = models.FloatField(default=0)
    deferredTax = models.FloatField(default=0)
    securityDeposit = models.FloatField(default=0)
    revaluationReserve = models.FloatField(default=0)
    totalOtherTermLiabilities = models.FloatField(default=0)

    def __str__(self):
        return f'Ocaocl {self.id}'