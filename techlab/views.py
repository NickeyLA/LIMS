from techlab.forms import TechlabForm
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from laboratory_gmc.models import Values
from main.models import Selection_point
from datetime import datetime, timedelta
import io
import json
import pandas as pd
from django.db.models import Avg, Min, Max


def _aware(dt):
    if dt and timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


@csrf_exempt
def download_excel_techlab(request):
    if request.method != "POST":
        return HttpResponse("Метод не поддерживается", status=405)

    try:
        data = json.loads(request.body)
        date_from = _aware(datetime.strptime(data["date_from"], "%Y-%m-%dT%H:%M"))
        date_to = _aware(datetime.strptime(data["date_to"], "%Y-%m-%dT%H:%M"))
        report_type = data.get("report_type", "day")
        points = data.get("points", [])

        if not points:
            return HttpResponse("Не выбраны точки и индикаторы", status=400)

        # Получаем queryset для всех выбранных точек
        all_point_ids = [p["point_id"] for p in points]
        values_qs = Values.objects.filter(
            selection_point_id__in=all_point_ids,
            user_defined_time__gte=date_from,
            user_defined_time__lte=date_to
        )

        # Словарь id -> имя точки
        points_objs = Selection_point.objects.filter(id__in=all_point_ids)
        points_map = {str(p.id): p.selection_point_name for p in points_objs}

        rows = []

        # ---------------- ДЕНЬ ----------------
        if report_type == "day":
            current_day = date_from.date()
            while current_day <= date_to.date():
                day_start = _aware(datetime.combine(current_day, date_from.time()))
                day_end = _aware(datetime.combine(current_day, date_to.time()))

                if current_day == date_from.date():
                    day_start = date_from
                if current_day == date_to.date():
                    day_end = date_to

                row = {
                    "Дата/Время": f"{day_start.strftime('%d.%m.%Y %H:%M')} - {day_end.strftime('%d.%m.%Y %H:%M')}"
                }

                for p in points:
                    point_id = str(p["point_id"])
                    point_name = points_map.get(point_id, f"Точка {point_id}")
                    for ind in p["indicators"]:
                        avg_val = values_qs.filter(
                            selection_point_id=point_id,
                            user_defined_time__gte=day_start,
                            user_defined_time__lte=day_end
                        ).aggregate(avg_val=Avg(ind))["avg_val"]
                        row[f"{point_name} - {ind}"] = round(avg_val, 2) if avg_val is not None else None

                rows.append(row)
                current_day += timedelta(days=1)

        # ---------------- МЕСЯЦ ----------------
        elif report_type == "month":
            current_month = datetime(date_from.year, date_from.month, 1, tzinfo=timezone.get_current_timezone())
            last_month = datetime(date_to.year, date_to.month, 1, tzinfo=timezone.get_current_timezone())

            while current_month <= last_month:
                # следующий месяц
                if current_month.month == 12:
                    next_month = datetime(current_month.year + 1, 1, 1, tzinfo=timezone.get_current_timezone())
                else:
                    next_month = datetime(current_month.year, current_month.month + 1, 1,
                                          tzinfo=timezone.get_current_timezone())

                month_start = max(current_month, date_from)
                month_end = min(next_month - timedelta(seconds=1), date_to)

                # среднее
                row_avg = {
                    "Период": f"{month_start.strftime('%d.%m.%y %H:%M')} - {month_end.strftime('%d.%m.%y %H:%M')}"}
                # минимум
                row_min = {"Период": "минимум"}
                # максимум
                row_max = {"Период": "максимум"}

                for p in points:
                    point_id = str(p["point_id"])
                    point_name = points_map.get(point_id, f"Точка {point_id}")
                    for ind in p["indicators"]:
                        agg = values_qs.filter(
                            selection_point_id=point_id,
                            user_defined_time__gte=month_start,
                            user_defined_time__lte=month_end
                        ).aggregate(
                            avg_val=Avg(ind),
                            min_val=Min(ind),
                            max_val=Max(ind)
                        )
                        row_avg[f"{point_name} - {ind}"] = round(agg["avg_val"], 2) if agg[
                                                                                           "avg_val"] is not None else None
                        row_min[f"{point_name} - {ind}"] = round(agg["min_val"], 2) if agg[
                                                                                           "min_val"] is not None else None
                        row_max[f"{point_name} - {ind}"] = round(agg["max_val"], 2) if agg[
                                                                                           "max_val"] is not None else None

                rows.append(row_avg)
                rows.append(row_min)
                rows.append(row_max)

                current_month = next_month


        # ---------------- ГОД ----------------
        elif report_type in ["year", "years"]:
            current_year = datetime(date_from.year, 1, 1, tzinfo=timezone.get_current_timezone())
            last_year = datetime(date_to.year, 1, 1, tzinfo=timezone.get_current_timezone())

            while current_year <= last_year:
                year_start = max(_aware(datetime(current_year.year, 1, 1)), date_from)
                year_end = min(_aware(datetime(current_year.year, 12, 31, 23, 59, 59)), date_to)

                row_avg = {"Период": f"{year_start.strftime('%d.%m.%y %H:%M')} - {year_end.strftime('%d.%m.%y %H:%M')}"}
                row_min = {"Период": "минимум"}
                row_max = {"Период": "максимум"}

                for p in points:
                    point_id = str(p["point_id"])
                    point_name = points_map.get(point_id, f"Точка {point_id}")
                    for ind in p["indicators"]:
                        agg = values_qs.filter(
                            selection_point_id=point_id,
                            user_defined_time__gte=year_start,
                            user_defined_time__lte=year_end
                        ).aggregate(
                            avg_val=Avg(ind),
                            min_val=Min(ind),
                            max_val=Max(ind)
                        )
                        row_avg[f"{point_name} - {ind}"] = round(agg["avg_val"], 2) if agg[
                                                                                           "avg_val"] is not None else None
                        row_min[f"{point_name} - {ind}"] = round(agg["min_val"], 2) if agg[
                                                                                           "min_val"] is not None else None
                        row_max[f"{point_name} - {ind}"] = round(agg["max_val"], 2) if agg[
                                                                                           "max_val"] is not None else None

                rows.append(row_avg)
                rows.append(row_min)
                rows.append(row_max)

                current_year = datetime(current_year.year + 1, 1, 1, tzinfo=timezone.get_current_timezone())

        else:
            return HttpResponse("Отчётный тип не поддерживается", status=400)

        # Создаём DataFrame
        df = pd.DataFrame(rows)

        # Пишем в Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Отчёт")

        buffer.seek(0)
        response = HttpResponse(
            buffer.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename=Выгрузка.xlsx'
        return response

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return HttpResponse(f"Ошибка при формировании отчёта: {e}", status=500)


def view_techlab_page(request):
    form = TechlabForm(request.GET or None)
    context = {'form': form}
    return render(request, 'techlab/techlab.html', context)
