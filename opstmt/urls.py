from django.urls import path
from .views import CreateCompanyView, GetCompaniesOpstmtView, UserLoginView, UpdateCompaniesOpstmtView,GetlatestCompanyView

urlpatterns = [
    path('create_company/<int:user_id>/', CreateCompanyView.as_view(), name='create_company'),
    path('get_companies_opstmt/<int:company_id>/', GetCompaniesOpstmtView.as_view(), name='get_companies_opstmt'),
    path('get_latest_company/<int:user_id>/', GetlatestCompanyView.as_view(), name='get_latest_company'),
    path('update_companies_opstmt/<int:company_id>/', UpdateCompaniesOpstmtView.as_view(),
         name='update_companies_opstmt'),
    path('login/', UserLoginView.as_view(), name='login')
]
