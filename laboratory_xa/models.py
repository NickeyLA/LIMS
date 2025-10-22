from django.db import models
from decimal import Decimal, getcontext
from decimal import Decimal, ROUND_HALF_UP
from main.models import *

class ValuesTitrLabXA(models.Model):
    fio = models.ForeignKey(Fio, on_delete=models.DO_NOTHING)
    titrant = models.ForeignKey(Titrant, on_delete=models.DO_NOTHING)
    t_titr = models.DecimalField(max_digits=10, decimal_places=7)
    v_titr_1 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    v_titr_2 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    v_titr_3 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    v_titr_4 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    used_values = models.CharField(max_length=10)
    user_defined_time = models.DateTimeField(null=False, blank=False)
    v_titr_medium = models.DecimalField(max_digits=10, decimal_places=7)
    delta = models.DecimalField(max_digits=10, decimal_places=7)
    created_at = models.DateTimeField(auto_now_add=True)


    def calculate_values_titr_XA(self):
        try:
            # Получаем значения, которые нужно использовать, на основе поля used_values
            used_indices = list(self.used_values)  # Преобразуем строку "124" в список ["1", "2", "4"]
            v_titr_values = []

            for index in used_indices:
                if index == "1" and self.v_titr_1 is not None:
                    v_titr_values.append(self.v_titr_1)
                elif index == "2" and self.v_titr_2 is not None:
                    v_titr_values.append(self.v_titr_2)
                elif index == "3" and self.v_titr_3 is not None:
                    v_titr_values.append(self.v_titr_3)
                elif index == "4" and self.v_titr_4 is not None:
                    v_titr_values.append(self.v_titr_4)

            if not v_titr_values:
                raise ValueError("Нет заполненных значений для расчета.")

            # Расчет дельты
            max_v_titr = max(v_titr_values)
            min_v_titr = min(v_titr_values)
            self.delta = max_v_titr - min_v_titr

            # Расчет среднего значения, если дельта <= 0.20
            if self.delta <= Decimal('0.20'):
                self.v_titr_medium = sum(v_titr_values) / Decimal(len(v_titr_values))
            else:
                # Если дельта больше 0.20, пользователь должен выбрать значения вручную
                self.v_titr_medium = None

            # Расчет t_titr в зависимости от титранта
            if self.v_titr_medium is not None:
                if self.titrant.titrant_name == "Соль Мора 0,07 моль/л":
                    self.t_titr = (Decimal('0.1') * Decimal('90.94') * Decimal('10')) / (self.v_titr_medium * Decimal('1000'))
                elif self.titrant.titrant_name == "Соль Мора 0,04 моль/л":
                    self.t_titr = (Decimal('0.1') * Decimal('90.94') * Decimal('5')) / (self.v_titr_medium * Decimal('1000'))
                elif self.titrant.titrant_name == "K2Cr2O7 0,025 моль/л":
                    self.t_titr = (Decimal('0.001') * Decimal('10')) / self.v_titr_medium
                elif self.titrant.titrant_name == "NaOH 0,6 моль/л":
                    self.t_titr = (Decimal('0.4') * Decimal('49') * Decimal('10')) / (self.v_titr_medium * Decimal('1000'))
                elif self.titrant.titrant_name == "NaOH 0,5 моль/л":
                    self.t_titr = (Decimal('1.000') * Decimal('0.8306')) / self.v_titr_medium
                elif self.titrant.titrant_name == "HCl 0,5 моль/л":
                    self.t_titr = (Decimal('0.5') * Decimal('0.01402')) / (self.v_titr_medium * Decimal('0.0265'))
                else:
                    self.t_titr = None
            else:
                self.t_titr = None

        except Exception as e:
            print(f"Ошибка при вычислении значений: {e}")

    def save(self, *args, **kwargs):

        print(4)
        """Перед сохранением пересчитываем расчетные показатели."""
        self.calculate_values_titr_XA()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.t_titr}"
