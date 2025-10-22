from django.urls import path  # Импортируем функцию path для определения маршрутов
from .views import main_page  # Импортируем наше представление main_page
from .views import lab_gmc_redirect  # Импортируем наше представление main_page
from .views import lab_xa_redirect  # Импортируем наше представление main_page
from .views import lab_otk_redirect  # Импортируем наше представление main_page

# Список маршрутов, доступных в приложении main
urlpatterns = [
    path('', main_page, name='home'),
    path('lab_gmc_redirect', lab_gmc_redirect, name='lab_gmc_redirect'),  # Перенаправление с /main/ на /lab/
    path('lab_xa_redirect', lab_xa_redirect, name='lab_xa_redirect'),  # Перенаправление с /main/ на /lab/
    path('lab_otk_redirect', lab_otk_redirect, name='lab_otk_redirect'),  # Перенаправление с /main/ на /lab/
]
