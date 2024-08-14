from django.urls import path
from .views import GetFFView, UpdateFFView

urlpatterns = [
    path('get_ff/<int:company_id>/', GetFFView.as_view(), name='get_ff'),
    path('update_ff/<int:company_id>/', UpdateFFView.as_view(), name='update_ff'),
]
