from django.urls import path
from .views import GetRatiosView
# , UpdateRatiosView
from . import views

urlpatterns = [
    path('get_ratios/<int:token_id>/', GetRatiosView.as_view(), name='get_ratios'),
    # path('update_ratios/<int:token_id>/', UpdateRatiosView.as_view(), name='update_ratios'),
    path('calculate_ratios/<str:pk>/', views.calculate_ratios, name='calculate_ratios')

]
