from django.urls import path
from .views import (
    analysis,
    gmc,
    download_analysis_excel,   # текущая точка скачивания (не трогаем)
    techlab,       # будет возвращать форму/фрагмент для модального окна
)

urlpatterns = [
    path('', analysis, name='analysis'),
    path('gmc/', gmc, name='gmc'),
    path('techlab/', techlab, name='techlab'),
    path('analysis/download/', download_analysis_excel, name='download_analysis_excel')
]