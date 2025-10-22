# viewer_gmc/views.py
import io
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Avg, Min, Max
from django.utils import timezone
from viewer_gmc.forms import ViewFormGMC
from laboratory_gmc.models import Values


# ----------------------------
# 🔹 Вспомогательные функции
# ----------------------------

def _aware(dt):
    """Делает дату aware, если она naive."""
    if dt and timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def decimal_to_float(value, digits=2):
    """Округляет Decimal в float для вывода и Excel."""
    if value is None:
        return None
    quantize_str = '0.' + '0' * digits
    return float(value.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP))


# ----------------------------
# 🔹 Общая логика фильтрации
# ----------------------------

def get_filtered_values(request):
    """Фильтрация и подготовка данных для таблицы и Excel."""
    form = ViewFormGMC(request.GET or None)

    # ❗ Сортировка теперь по ID (по убыванию)
    values_qs = Values.objects.exclude(
        id__in=Values.objects.exclude(replaced_by__isnull=True)
        .values_list('replaced_by', flat=True)
    ).select_related(
        'selection_point', 'replaced_by', 'indicator'
    ).order_by('-id')

    # Применяем фильтры
    if form.is_valid():
        if form.cleaned_data.get('selection_point'):
            values_qs = values_qs.filter(selection_point=form.cleaned_data['selection_point'])
        if form.cleaned_data.get('date_from'):
            values_qs = values_qs.filter(user_defined_time__gte=_aware(form.cleaned_data['date_from']))
        if form.cleaned_data.get('date_to'):
            values_qs = values_qs.filter(user_defined_time__lte=_aware(form.cleaned_data['date_to']))

    # Подготовка списка для отображения
    values_list = []
    for v in values_qs[:1000]:
        values_list.append({
            'id': v.id,
            'user_defined_time': v.user_defined_time,
            'created_at': v.created_at,
            'selection_point': v.selection_point.selection_point_name if v.selection_point else None,
            'ph': decimal_to_float(v.ph, 2),
            'v2o5': decimal_to_float(v.v2o5, 2),
            'h2so4': decimal_to_float(v.h2so4, 2),
            'mgso4': decimal_to_float(v.mgso4, 2),
            'susp': decimal_to_float(v.susp, 3),
            'dry_residue': decimal_to_float(v.dry_residue, 2),
            'replace_source': v.replace_source,
            'replaced_by_id': v.replaced_by.id if v.replaced_by else None,
        })

    # Статистика
    stats = values_qs.aggregate(
        avg_ph=Avg('ph'), min_ph=Min('ph'), max_ph=Max('ph'),
        avg_v2o5=Avg('v2o5'), min_v2o5=Min('v2o5'), max_v2o5=Max('v2o5'),
        avg_h2so4=Avg('h2so4'), min_h2so4=Min('h2so4'), max_h2so4=Max('h2so4'),
        avg_mgso4=Avg('mgso4'), min_mgso4=Min('mgso4'), max_mgso4=Max('mgso4'),
        avg_susp=Avg('susp'), min_susp=Min('susp'), max_susp=Max('susp'),
        avg_dry_residue=Avg('dry_residue'),
        min_dry_residue=Min('dry_residue'),
        max_dry_residue=Max('dry_residue'),
    )

    return form, values_list, stats


# ----------------------------
# 🔹 Отображение страницы
# ----------------------------

def viewer_gmc_page(request):
    form, values_list, stats = get_filtered_values(request)
    context = {'form': form, 'values_list': values_list, 'stats': stats}
    return render(request, 'viewer_gmc/viewer_gmc.html', context)


# ----------------------------
# 🔹 Выгрузка в Excel
# ----------------------------

def download_excel_viewer_gmc(request):
    """Выгрузка в Excel с указанием 'Факт. время'."""
    form = ViewFormGMC(request.GET or None)

    # ❗ Та же сортировка по ID
    values_qs = Values.objects.exclude(
        id__in=Values.objects.exclude(replaced_by__isnull=True)
        .values_list('replaced_by', flat=True)
    ).select_related('selection_point', 'replaced_by', 'indicator').order_by('-id')

    # Применяем фильтры
    if form.is_valid():
        if form.cleaned_data.get('selection_point'):
            values_qs = values_qs.filter(selection_point=form.cleaned_data['selection_point'])
        if form.cleaned_data.get('date_from'):
            values_qs = values_qs.filter(user_defined_time__gte=_aware(form.cleaned_data['date_from']))
        if form.cleaned_data.get('date_to'):
            values_qs = values_qs.filter(user_defined_time__lte=_aware(form.cleaned_data['date_to']))

    # --- Формируем DataFrame ---
    df = pd.DataFrame(list(values_qs.values(
        'id',
        'user_defined_time',
        'created_at',
        'selection_point__selection_point_name',
        'ph', 'v2o5', 'h2so4', 'mgso4', 'susp', 'dry_residue',
        'replace_source', 'replaced_by__id',
    )))

    # --- Форматируем время ---
    for col in ['user_defined_time', 'created_at']:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda dt: dt.strftime("%d.%m.%Y %H:%M:%S") if pd.notnull(dt) else ""
            )

    # --- Преобразуем числовые колонки ---
    for col in ['ph', 'v2o5', 'h2so4', 'mgso4', 'dry_residue']:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: float(Decimal(x).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                if x not in (None, '') else None
            )
    for col in ['susp']:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: float(Decimal(x).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
                if x not in (None, '') else None
            )

    # --- Переименование колонок ---
    df.rename(columns={
        'id': 'ID',
        'user_defined_time': 'Указанное время',
        'created_at': 'Факт. время',
        'selection_point__selection_point_name': 'Точка отбора',
        'ph': 'pH',
        'v2o5': 'V2O5 г/л',
        'h2so4': 'H2SO4 г/л',
        'mgso4': 'MgSO4 г/л',
        'susp': 'Взвесь г/л',
        'dry_residue': 'Сухой остаток г/л',
        'replace_source': 'Источник замены',
        'replaced_by__id': 'ID Замененной записи',
    }, inplace=True)

    # --- Записываем в Excel ---
    with io.BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine='xlsxwriter', datetime_format='dd.mm.yyyy hh:mm:ss') as writer:
            df.to_excel(writer, index=False, sheet_name='Результаты')
            worksheet = writer.sheets['Результаты']
            worksheet.set_column('A:Z', 18)
        buffer.seek(0)

        response = HttpResponse(
            buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=результаты_анализов.xlsx'
        return response
