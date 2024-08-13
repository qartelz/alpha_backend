from django.urls import path
from .views import GetAssetnLiabsView, UpdateAssetnLiabsView
from . import views

urlpatterns = [
    path('get_assetnliabs/<int:company_id>/', GetAssetnLiabsView.as_view(), name='get_companies_assetnliabs'),
    path('update_assetnliabs/<int:company_id>/', UpdateAssetnLiabsView.as_view(), name='update_companies_assetnliabs'),
    #path('assetnliabscalculation/<str:company_ids>/', views.assetnliabscalculation, name='assetnliabscalculation')
]
