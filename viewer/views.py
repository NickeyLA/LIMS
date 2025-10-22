from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
import io, re
import pandas as pd
from django.db.models import Avg, Min, Max, FloatField, Value
from django.db.models.functions import Cast, Replace
from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.models import AnalysisResults
from .forms import ViewForm
from django.utils.timezone import is_naive, make_aware, get_default_timezone
from datetime import timedelta


# ----------------------------
# Вспомогательные функции
# ----------------------------

def format_dt(dt):
    """Локализованное время (например, user_defined_time)."""
    if not dt:
        return ''
    try:
        if is_naive(dt):
            dt = make_aware(dt, timezone=get_default_timezone())
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return str(dt)


def format_dt_shifted(dt, hours=3):
    """Время с добавкой часов, например для Факт. отбор и Факт. анализ."""
    if not dt:
        return ''
    try:
        dt_shifted = dt + timedelta(hours=hours)
        return dt_shifted.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return str(dt)


def round_value(v, digits=2):
    """Безопасное округление чисел."""
    try:
        return str(Decimal(v).quantize(Decimal(f"0.{ '0'*digits }"), rounding=ROUND_HALF_UP))
    except Exception:
        return v


def clean_name_value(name_value: str) -> str:
    """Очищает текст показателя от '(вычисл)'."""
    if not name_value:
        return ''
    return re.sub(r'\s*\(?вычисл\)?', '', name_value, flags=re.IGNORECASE).strip()


def process_result(res, shift_hours=3):
    """Обрабатывает один результат анализа и возвращает словарь с подготовленными полями."""
    probe = res.probe_indicator.probe
    indicator = res.probe_indicator.indicator.indicator_name

    timestamp_probe_defined = format_dt(probe.user_defined_time)
    timestamp_probe_fact = format_dt_shifted(probe.created_at, hours=shift_hours)
    timestamp_analys_fact = format_dt_shifted(res.created_at, hours=shift_hours)

    name_value = res.name_value or ''
    is_calculated = '(вычисл' in name_value.lower()
    value_rounded = round_value(res.value, 2)

    return {
        'probe_code': probe.code,
        'selection_point': probe.selection_point.selection_point_name,
        'name_probe': probe.name_probe,
        'fio': res.fio.fio,
        'indicator': indicator,
        'name_value': name_value,
        'value': value_rounded,
        'timestamp_probe_defined': timestamp_probe_defined,
        'timestamp_probe_fact': timestamp_probe_fact,
        'timestamp_analys_fact': timestamp_analys_fact,
        'is_calculated': is_calculated,
    }


# ----------------------------
# Перенаправления
# ----------------------------

def gmc(request):
    return redirect('viewer_gmc_page')


def techlab(request):
    return redirect('view_techlab_page')


# ----------------------------
# Просмотр анализов
# ----------------------------

def analysis(request):
    form = ViewForm(request.GET or None)
    qs = AnalysisResults.objects.filter(is_deleted=False).select_related(
        'probe_indicator__probe__selection_point',
        'probe_indicator__indicator',
        'fio'
    )

    stats, stats_indicator_name, stats_from_computed = None, None, False

    if form.is_valid():
        selection_point = form.cleaned_data.get('selection_point')
        indicator = form.cleaned_data.get('indicator')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if selection_point:
            qs = qs.filter(probe_indicator__probe__selection_point=selection_point)
        if indicator:
            qs = qs.filter(probe_indicator__indicator=indicator)
            stats_indicator_name = indicator.indicator_name
        if date_from:
            qs = qs.filter(user_defined_time__gte=date_from)
        if date_to:
            qs = qs.filter(user_defined_time__lte=date_to)

        # Статистика
        if indicator:
            pattern = rf'^\s*{re.escape(stats_indicator_name)}.*\(вычисл\)\s*$'
            numeric_qs = qs.filter(name_value__iregex=pattern)
            if not numeric_qs.exists():
                numeric_qs = qs

            numeric_qs = numeric_qs.filter(value__regex=r'^[+-]?\d+(?:[.,]\d+)?$')
            numeric_qs = numeric_qs.annotate(
                value_norm=Replace('value', Value(','), Value('.')),
                value_num=Cast('value_norm', FloatField())
            )

            stats_raw = numeric_qs.aggregate(
                avg_value=Avg('value_num'),
                min_value=Min('value_num'),
                max_value=Max('value_num'),
            )

            stats = {k: (round_value(v, 2) if v is not None else None) for k, v in stats_raw.items()}

    qs = qs.order_by(
        '-probe_indicator__probe__id',
        'probe_indicator__indicator__indicator_name',
        '-created_at',
    )

    # Группировка
    temp_grouped = defaultdict(lambda: defaultdict(list))
    probe_ids = {}

    for res in qs:
        data = process_result(res, shift_hours=3)
        probe_ids[data['probe_code']] = res.probe_indicator.probe.id
        temp_grouped[data['probe_code']][data['indicator']].append(data)

    # Построение структуры для шаблона
    final_grouped_analysis = []
    for probe_code in sorted(temp_grouped.keys(), key=lambda c: probe_ids[c], reverse=True):
        probe_data = temp_grouped[probe_code]
        probe_rows, total_probe_rows = [], 0

        for indicator_name, vals in probe_data.items():
            computed_vals = [v for v in vals if v['is_calculated']]
            display_vals = computed_vals if computed_vals else vals
            total_probe_rows += len(display_vals)

        first_probe_row = True
        for indicator_name, vals in probe_data.items():
            computed_vals = [v for v in vals if v['is_calculated']]
            display_vals = computed_vals if computed_vals else vals
            first_indicator_row = True
            indicator_rowspan = len(display_vals)

            for val in display_vals:
                probe_rows.append({
                    'probe_code': probe_code,
                    'selection_point': val['selection_point'],
                    'name_probe': val['name_probe'],
                    'indicator': indicator_name,
                    'value_combined': f"{clean_name_value(val['name_value'])} – {val['value']}",
                    'timestamp_probe_defined': val['timestamp_probe_defined'],
                    'timestamp_probe_fact': val['timestamp_probe_fact'],
                    'timestamp_analys_fact': val['timestamp_analys_fact'],
                    'is_first_probe_group_row': first_probe_row,
                    'probe_group_rowspan': total_probe_rows if first_probe_row else 0,
                    'is_first_indicator_row': first_indicator_row,
                    'indicator_rowspan': indicator_rowspan if first_indicator_row else 0,
                })
                first_probe_row = False
                first_indicator_row = False

        final_grouped_analysis.append(probe_rows)

    context = {
        'form': form,
        'grouped_analysis': final_grouped_analysis,
        'stats': stats,
        'stats_indicator_name': stats_indicator_name,
        'stats_from_computed': stats_from_computed,
    }
    return render(request, 'viewer/analysis.html', context)


# ----------------------------
# Выгрузка в Excel
# ----------------------------
def download_analysis_excel(request):
    form = ViewForm(request.GET or None)
    qs = AnalysisResults.objects.filter(is_deleted=False).select_related(
        'probe_indicator__probe__selection_point',
        'probe_indicator__indicator',
        'fio'
    ).order_by(
        '-probe_indicator__probe__id',
        'probe_indicator__indicator__indicator_name',
        '-created_at',
    )

    if form.is_valid():
        selection_point = form.cleaned_data.get('selection_point')
        indicator = form.cleaned_data.get('indicator')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if selection_point:
            qs = qs.filter(probe_indicator__probe__selection_point=selection_point)
        if indicator:
            qs = qs.filter(probe_indicator__indicator=indicator)
        if date_from:
            qs = qs.filter(user_defined_time__gte=date_from)
        if date_to:
            qs = qs.filter(user_defined_time__lte=date_to)

    temp_grouped = defaultdict(lambda: defaultdict(list))
    probe_ids = {}

    def safe_float(val):
        """Пробуем преобразовать значение в float для Excel, иначе возвращаем строку"""
        if val is None:
            return None
        try:
            val_str = str(val).replace(',', '.')
            return float(val_str)
        except Exception:
            return val

    for res in qs:
        data = process_result(res, shift_hours=3)
        data['value'] = safe_float(data['value'])  # безопасное преобразование
        probe_ids[data['probe_code']] = res.probe_indicator.probe.id
        temp_grouped[data['probe_code']][data['indicator']].append(data)

    excel_rows = []
    for probe_code in sorted(temp_grouped.keys(), key=lambda c: probe_ids[c], reverse=True):
        probe_data = temp_grouped[probe_code]
        first_probe_row = True

        for indicator_name, vals in probe_data.items():
            computed_vals = [v for v in vals if v['is_calculated']]
            display_vals = computed_vals if computed_vals else vals
            first_indicator_row = True

            for val in display_vals:
                excel_rows.append({
                    'Шифр пробы': probe_code if first_probe_row else '',
                    'Точка отбора': val['selection_point'] if first_probe_row else '',
                    'Наименование пробы': val['name_probe'] if first_probe_row else '',
                    'Показатель': indicator_name if first_indicator_row else '',
                    'Название': val['name_value'],
                    'Значение': val['value'],  # float или оставляем строку
                    'Указ. отбор': val['timestamp_probe_defined'],
                    'Факт. отбор': val['timestamp_probe_fact'],
                    'Факт. анализ': val['timestamp_analys_fact'],
                })
                first_probe_row = False
                first_indicator_row = False

    df = pd.DataFrame(excel_rows)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter', datetime_format='dd.mm.yyyy hh:mm:ss') as writer:
        df.to_excel(writer, index=False, sheet_name='Результаты')
        worksheet = writer.sheets['Результаты']
        worksheet.set_column('A:I', 20)

    buffer.seek(0)
    response = HttpResponse(
        buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=анализы.xlsx'
    return response
