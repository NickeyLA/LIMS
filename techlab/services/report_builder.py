# techlab/services/report_builder.py
import pandas as pd
from django.db.models import Avg
from .models import Values


class ReportBuilder:
    def __init__(self, intervals, selection_points, indicators):
        """
        :param intervals: список кортежей (start_datetime, end_datetime)
        :param selection_points: список selection_point (id или имена)
        :param indicators: список indicator (id или имена)
        """
        self.intervals = intervals
        self.selection_points = selection_points
        self.indicators = indicators

    def _get_data_for_interval(self, start, end):
        """Фильтруем данные из БД и возвращаем средние значения"""
        qs = Values.objects.filter(
            user_defined_time__range=(start, end),
            selection_point_id__in=self.selection_points,
            indicator_id__in=self.indicators
        )

        # агрегируем
        data = (
            qs.values("selection_point__name", "indicator__indicator_name")
              .annotate(avg_value=Avg("ph"))  # ⚠️ пока считаем только pH, нужно расширить
        )

        df = pd.DataFrame(list(data))
        return df

    def build(self):
        """Формируем общую таблицу"""
        frames = []
        for start, end in self.intervals:
            df = self._get_data_for_interval(start, end)
            if df.empty:
                continue

            # добавляем колонку периода
            df["period"] = f"{start:%d.%m.%y %H:%M} – {end:%d.%m.%y %H:%M}"
            frames.append(df)

        if not frames:
            return pd.DataFrame()

        df_all = pd.concat(frames)

        # сводная таблица: строки = период, столбцы = (selection_point, indicator)
        pivot = df_all.pivot_table(
            index="period",
            columns=["selection_point__name", "indicator__indicator_name"],
            values="avg_value",
            aggfunc="mean"
        )

        # приводим вид заголовков к привычному (многоуровневые)
        pivot.columns = pd.MultiIndex.from_tuples(pivot.columns)

        return pivot.reset_index()
