from django.urls import path
from .views import get_revenue_from_operations, get_pbt_and_pbt, get_current_ratio, get_pbdit, get_net_cash_accruals, get_cash_accruals, get_net_working_capital

urlpatterns = [
    path('revenue_from_operations-data/<int:company_id>/', get_revenue_from_operations, name='revenue_from_operations-data'),
    path('pbt_and_pat/<int:company_id>/', get_pbt_and_pbt, name='get_pbt_and_pbt'),
    path('current_ratio/<int:company_id>/', get_current_ratio, name='get_current_ratio'),
    path('get_pbdit/<int:company_id>/', get_pbdit, name='get_pbdit'),
    path('get_cash_accruals/<int:company_id>/', get_cash_accruals, name='get_cash_accruals'),
    path('get_net_working_capital/<int:company_id>/', get_net_working_capital, name='get_net_working_capital'),
    path('get_net_cash_accruals/<int:company_id>/', get_net_cash_accruals, name='get_net_cash_accruals'),
]
