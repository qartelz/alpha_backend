# Generated by Django 5.1 on 2024-08-10 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('opstmt', '0003_alter_year_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='OcaOcl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cashAndBankBalance', models.FloatField(default=0)),
                ('fixedDepositsWithBank', models.FloatField(default=0)),
                ('advanceIncomeTaxSalesTax', models.FloatField(default=0)),
                ('advanceToStaffDirectors', models.FloatField(default=0)),
                ('advanceToSuppliers', models.FloatField(default=0)),
                ('exciseCustomsTuf', models.FloatField(default=0)),
                ('loansAndAdvances', models.FloatField(default=0)),
                ('others', models.FloatField(default=0)),
                ('totalOtherCurrentAssets', models.FloatField(default=0)),
                ('securityDepositsEbEtc', models.FloatField(default=0)),
                ('loanAndAdvances', models.FloatField(default=0)),
                ('sundryDebtorsGreater6months', models.FloatField(default=0)),
                ('investment', models.FloatField(default=0)),
                ('interestAccruedOnLoans', models.FloatField(default=0)),
                ('othersNonCurrent', models.FloatField(default=0)),
                ('totalNonCurrentAssets', models.FloatField(default=0)),
                ('tlInstDueIn1YearIob', models.FloatField(default=0)),
                ('tlInstDueIn1YearBankInst', models.FloatField(default=0)),
                ('sundryCreditorsExpenses', models.FloatField(default=0)),
                ('expensesPayable', models.FloatField(default=0)),
                ('provisionForTaxEtc', models.FloatField(default=0)),
                ('othersCurrentLiabilities', models.FloatField(default=0)),
                ('totalOtherCurrentLiabilities', models.FloatField(default=0)),
                ('otherTermLiabilities', models.FloatField(default=0)),
                ('unsecuredLoanPromotors', models.FloatField(default=0)),
                ('deferredTax', models.FloatField(default=0)),
                ('securityDeposit', models.FloatField(default=0)),
                ('revaluationReserve', models.FloatField(default=0)),
                ('totalOtherTermLiabilities', models.FloatField(default=0)),
                ('year', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ocaocl', to='opstmt.year')),
            ],
        ),
    ]
