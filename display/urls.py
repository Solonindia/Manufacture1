from django.urls import path
from .views import production_dashboard, save_data

urlpatterns = [
    path('', production_dashboard, name='production_dashboard'),
    path('save-data/', save_data, name='save_data'),
]