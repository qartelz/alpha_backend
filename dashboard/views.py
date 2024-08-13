from django.shortcuts import render
from opstmt.models import Company, Opstmt, Year
from django.http import JsonResponse


# Create your views here.
def get_revenue_from_operations(request, company_id):
    company = Company.objects.get(id = company_id)
    years = company.years.all() 

    # Prepare the data
    data = [
        {
            'company': year.year,
            'revenue': year.opstmt.total_sales  # Access the related Opstmt model
        }
        for year in years
    ]

    # Return the data as JSON response
    return JsonResponse(data, safe=False)


def get_pbt_and_pbt(request, company_id):
    company = Company.objects.get(id = company_id)
    years = company.years.all()
    # Prepare the data
    data = [
        {
            'company': year.year,
            'pbt': year.opstmt.profit_before_tax,  # Access the related Opstmt model
            'pat': year.opstmt.net_profit_after_tax_loss  # Access the related Opstmt model
        }
        for year in years
    ]

    # Return the data as JSON response
    return JsonResponse(data, safe=False)


def get_current_ratio(request, company_id):
    company = Company.objects.get(id = company_id)
    years = company.years.all()
    # Prepare the data
    data = [
        {
            'company': year.year,
            'current_ratio': year.ratios.current_ratio,  
        }
        for year in years
    ]

    return JsonResponse(data, safe=False)


# Create your views here.
def get_pbdit(request, company_id):
    company = Company.objects.get(id = company_id)
    years = company.years.all()
    # Prepare the data
    data = [
        {
            'company': year.year,
            'pbdit': year.opstmt.pbd_it  
        }
        for year in years
    ]

    return JsonResponse(data, safe=False)


def get_cash_accruals(request, company_id):
    company = Company.objects.get(id = company_id)
    years = company.years.all()

    # Prepare the data
    data = [
        {
            'company': year.year,
            'cash_accruals': year.opstmt.cash_accruals  
        }
        for year in years
    ]

    return JsonResponse(data, safe=False)


def get_net_working_capital(request, company_id):
    company = Company.objects.get(id = company_id)
    years = company.years.all()

    # Prepare the data
    data = [
        {
            'company': year.year,
            'net_working_capital': year.kfi.net_working_capital  
        }
        for year in years
    ]

    return JsonResponse(data, safe=False)


def get_net_cash_accruals(request, company_id):
    company = Company.objects.get(id = company_id)
    years = company.years.all()
    # Prepare the data
    data = [
        {
            'company': year.year,
            'net_working_capital': year.opstmt.net_cash_accrual  
        }
        for year in years
    ]

    return JsonResponse(data, safe=False)