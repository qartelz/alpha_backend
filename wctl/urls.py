from django.urls import path
from .views import GetWcTlView
# , UpdateWcTlView

urlpatterns = [
    path('get_wctl/<int:token_id>/', GetWcTlView.as_view(), name='get_wctl'),
    # path('update_wctl/<int:token_id>/', UpdateWcTlView.as_view(), name='update_wctl'),
]
