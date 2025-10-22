from django.shortcuts import render, redirect
from django.contrib import messages
from laboratory_otk.forms import *  # Импортируем все формы
from main.models import Probes, AnalysisResults, ProbeIndicator  # Импортируем модели
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def lab_otk_page(request):
    if request.method == 'POST':
        if 'form_type' in request.POST and request.POST['form_type'] == 'prob_form':
            probe_count = int(request.POST.get('probe_count', 1))  # Получаем количество проб, по умолчанию 1
            if probe_count < 1:
                messages.error(request, 'Количество проб должно быть больше 0')
                return redirect('lab_otk_page')

            created_probes = []
            post_data = request.POST.copy()  # Создаем копию POST-данных
            for _ in range(probe_count):
                prob_form = ProbForm(post_data)  # Создаем новый экземпляр формы
                if prob_form.is_valid():
                    probe = prob_form.save(commit=False)  # Создаем объект без сохранения
                    probe.save()                          # Сохраняем основную модель
                    prob_form.save_m2m()                  # Сохраняем ManyToMany (показатели)
                    created_probes.append(probe.code)
                else:
                    messages.error(request, f'Ошибка валидации формы: {prob_form.errors}')
                    return redirect('lab_otk_page')

            messages.success(request, f'Зарегистрировано {probe_count} проб: {", ".join(created_probes)}')
            return redirect('lab_otk_page')
    else:
        probform = ProbForm()
        prob_list = Probes.objects.all().order_by('-created_at')[:100]

        context = {
            'probform': probform,
            'prob_list': prob_list,
        }
        return render(request, 'laboratory_otk/index.html', context)


@require_POST
def delete_probe(request):
    probe_id = request.POST.get('probe_id')
    if not probe_id:
        return JsonResponse({'error': 'ID пробы не передан'}, status=400)

    try:
        probe = Probes.objects.get(id=probe_id)
        # Проверяем, есть ли связанные результаты анализа
        if AnalysisResults.objects.filter(probe_indicator__probe=probe).exists():
            return JsonResponse({'error': 'Нельзя удалить пробу, так как существуют связанные результаты анализа'}, status=400)
        probe.delete()
        return JsonResponse({'status': 'ok', 'deleted': 1})
    except Probes.DoesNotExist:
        return JsonResponse({'error': 'Проба не найдена'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Ошибка при удалении: {str(e)}'}, status=500)

