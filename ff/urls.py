from django.urls import path
from .views import GetFFView
# , UpdateKFIView

urlpatterns = [
    path('get_ff/<int:company_id>/', GetFFView.as_view(), name='get_ff'),
    # path('update_kfi/<int:company_id>/', UpdateKFIView.as_view(), name='update_kfi'),
]
