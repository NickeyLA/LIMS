from django.shortcuts import render, redirect
from laboratory_xa.forms import ValuesTitrFormXA, AnalysisResultForm
from laboratory_xa.models import ValuesTitrLabXA
from main.models import ProbeIndicator, Probes
from django.http import JsonResponse
from .analysis_templates import ANALYSIS_TEMPLATES
from .analysis_calculations import *
from django.views.decorators.http import require_POST
from .models import AnalysisResults
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP


@require_POST
def save_analysis(request):
    name_values = request.POST.getlist('name_value')
    values = request.POST.getlist('value')
    fio = request.POST.get('fio')
    probe_indicator = request.POST.get('probe_indicator')
    user_defined_time = parse_datetime(request.POST.get('user_defined_time'))
    selected_indicator = request.POST.get('selected_indicator')
    selection_point = request.POST.get('selection_point')

    if user_defined_time is not None and is_naive(user_defined_time):
        user_defined_time = make_aware(user_defined_time)

    if not fio or not probe_indicator or not user_defined_time:
        return JsonResponse({'errors': {
            'fio': 'Обязательное поле',
            'probe_indicator': 'Обязательное поле',
            'user_defined_time': 'Обязательное поле'
        }}, status=400)

    if len(name_values) != len(values):
        return JsonResponse({'errors': 'Количество показателей не совпадает с количеством значений'}, status=400)

    input_data = {}
    for name, value in zip(name_values, values):
        if not value.strip() or not name.strip():
            continue
        try:
            input_data[name] = float(value.replace(",", "."))
        except ValueError:
            input_data[name] = value

    template = ANALYSIS_TEMPLATES.get((selected_indicator, selection_point))

    if template and template.get("formula"):
        formula_func = globals().get(template["formula"])
        if not formula_func:
            return JsonResponse({'errors': f'Формула "{template["formula"]}" не найдена'}, status=500)

        try:
            result, titr_record = formula_func(input_data)
            if "Ошибка" in result:
                return JsonResponse({'errors': result}, status=400)

            result_name, result_value = next(iter(result.items()))
        except Exception as e:
            return JsonResponse({'errors': f'Ошибка при расчёте: {str(e)}'}, status=500)

        if titr_record:
            AnalysisResults.objects.create(
                fio_id=fio,
                probe_indicator_id=probe_indicator,
                user_defined_time=user_defined_time,
                name_value=titr_record.titrant.titrant_name,
                value=titr_record.t_titr
            )

    for name, value in zip(name_values, values):
        if not value.strip() or not name.strip():
            continue
        AnalysisResults.objects.create(
            fio_id=fio,
            probe_indicator_id=probe_indicator,
            user_defined_time=user_defined_time,
            name_value=name,
            value=value
        )

    if template and template.get("formula"):
        AnalysisResults.objects.create(
            fio_id=fio,
            probe_indicator_id=probe_indicator,
            user_defined_time=user_defined_time,
            name_value=result_name,
            value=result_value
        )

    return JsonResponse({'status': 'ok'})

def lab_xa_page(request):
    if request.method == 'POST':
        if 'form_type' in request.POST and request.POST['form_type'] == 'titrant_form_xa':
            titrant_form_xa = ValuesTitrFormXA(request.POST)
            if titrant_form_xa.is_valid():
                titrant_form_xa.save()
                return redirect('lab_xa_page')

    else:
        titrant_form_xa = ValuesTitrFormXA()
        analysis_form_xa = AnalysisResultForm()
        titrant_list_xa = ValuesTitrLabXA.objects.order_by('titrant_id', '-created_at').distinct('titrant_id')
        analysis_list_xa = AnalysisResults.objects.all()
        last_entry = ValuesTitrLabXA.objects.order_by('-created_at').first()
        last_analysis = AnalysisResults.objects.order_by('-created_at').first()

        context = {
            'analysis_form_xa': analysis_form_xa,
            'analysis_list_xa': analysis_list_xa,
            'titrant_list_xa': titrant_list_xa,
            'titrant_form_xa': titrant_form_xa,
            'last_fio_titr': last_entry.fio.id if last_entry else None,
            'last_fio': last_analysis.fio.id if last_analysis else '',
            'last_probe': last_analysis.probe_indicator.probe.id if last_analysis else '',
        }

        return render(request, 'laboratory_xa/index.html', context)


def get_probe_data(request, probe_id):
    probe_indicators = ProbeIndicator.objects.filter(probe_id=probe_id).select_related('indicator')

    try:
        probe = Probes.objects.select_related('selection_point').get(id=probe_id)
        analysis_rows = AnalysisResults.objects.filter(
            probe_indicator__probe_id=probe_id,
            is_deleted=False
        ).select_related('probe_indicator__indicator', 'fio')

        grouped_results = defaultdict(list)
        for row in analysis_rows:
            grouped_results[row.probe_indicator_id].append(row)

        analysis_results = []
        for probe_indicator_id, group in grouped_results.items():
            first = group[0]
            analysis_results.append({
                "probe_indicator_id": probe_indicator_id,
                "indicator_name": first.probe_indicator.indicator.indicator_name,
                "selection_point_name": first.probe_indicator.probe.selection_point.selection_point_name,
                "name_probe": first.probe_indicator.probe.name_probe,
                "fio": str(first.fio),
                "user_defined_time": first.user_defined_time.strftime('%Y-%m-%d %H:%M'),
                "values": [
                    {"name": r.name_value, "value": r.value}
                    for r in group
                ]
            })

        selection_point = probe.selection_point.selection_point_name
        probe_datetime = probe.user_defined_time.strftime('%Y-%m-%d %H:%M') if probe.user_defined_time else None
        comment = probe.comment
        name_probe = probe.name_probe
        comment_for_lab = probe.comment_for_lab

    except Probes.DoesNotExist:
        return JsonResponse({'error': 'Проба не найдена'}, status=404)

    indicators_data = []
    for pi in probe_indicators:
        used_probe_indicator_ids = set(
            AnalysisResults.objects.filter(probe_indicator__probe_id=probe_id, is_deleted=False)
            .values_list('probe_indicator_id', flat=True)
        )

        if pi.id in used_probe_indicator_ids:
            continue

        indicator_name = pi.indicator.indicator_name
        template = ANALYSIS_TEMPLATES.get((indicator_name, selection_point))
        indicators_data.append({
            'id': pi.id,
            'name': indicator_name,
            'template': template
        })

    return JsonResponse({
        'selection_point': selection_point,
        'probe_datetime': probe_datetime,
        'indicators': indicators_data,
        'analysis_results': analysis_results,
        'comment': comment,
        'name_probe': probe.name_probe,
        'comment_for_lab': comment_for_lab
    })


def delete_analysis_results_by_probe_indicator(request):
    if request.method == 'POST':
        probe_indicator_id = request.POST.get('probe_indicator_id')
        if not probe_indicator_id:
            return JsonResponse({'error': 'ID не передан'}, status=400)

        deleted_count = AnalysisResults.objects.filter(
            probe_indicator_id=probe_indicator_id
        ).update(is_deleted=True)

        return JsonResponse({'status': 'ok', 'deleted': deleted_count})

    return JsonResponse({'error': 'Неверный метод запроса'}, status=405)

