from django.urls import path
from .views import GetKFIView
# , UpdateKFIView

urlpatterns = [
    path('get_kfi/<int:company_id>/', GetKFIView.as_view(), name='get_kfi'),
    # path('update_kfi/<int:company_id>/', UpdateKFIView.as_view(), name='update_kfi'),
]
