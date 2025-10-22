from django.urls import path
from .views import viewer_gmc_page, download_excel_viewer_gmc  # импортируем view

urlpatterns = [
    path('', viewer_gmc_page, name='viewer_gmc_page'),
    path('download/', download_excel_viewer_gmc, name='viewer_gmc_download_excel'),
]