from django.urls import path
from .views import BulkHospitalCreateView

app_name = 'bulk'

urlpatterns = [
    path('hospitals/bulk', BulkHospitalCreateView.as_view(), name='bulk_create'),
]
