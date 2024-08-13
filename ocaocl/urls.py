from django.urls import path
from .views import GetOcaOclView, UpdateOcaOclView

urlpatterns = [
    path('get_ocaocl/<int:company_id>/', GetOcaOclView.as_view(), name='get_ocaocl'),
    path('update_ocaocl/<int:company_id>/', UpdateOcaOclView.as_view(), name='update_ocaocl'),
]
