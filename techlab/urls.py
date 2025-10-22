from django.urls import path
from .views import view_techlab_page
from .views import download_excel_techlab


urlpatterns = [
    path('', view_techlab_page, name='view_techlab_page'),
    path('download-excel/', download_excel_techlab, name='download_excel_techlab'),
]