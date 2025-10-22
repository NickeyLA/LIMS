from django.urls import path
from .views import lab_otk_page, delete_probe

urlpatterns = [
    path('', lab_otk_page, name="lab_otk_page"),
    path('delete_probe/', delete_probe, name="delete_probe")
]