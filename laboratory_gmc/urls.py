from django.urls import path
from .views import lab_page
from .views import get_record_data

urlpatterns = [
    path('', lab_page, name='lab_page'),
    path('get-record-data/<int:record_id>/', get_record_data, name='get_record_data'),
]
