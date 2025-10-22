from django.shortcuts import render  # Импортируем функцию render для отображения шаблонов
from django.shortcuts import redirect

# Определяем функцию для обработки запросов на главную страницу
def main_page(request):
    return render(request, 'main/index.html')

def lab_gmc_redirect(request):
    return redirect('lab_page')  # 'lab_index' — это имя маршрута из urls.py приложения Laboratory_GMC

def lab_xa_redirect(request):
    return redirect('lab_xa_page')  # 'lab_index' — это имя маршрута из urls.py приложения Laboratory_GMC

def lab_otk_redirect(request):
    return redirect('lab_otk_page')  # 'lab_index' — это имя маршрута из urls.py приложения Laboratory_GMC
