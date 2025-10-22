from django.db import models
from decimal import Decimal, getcontext
from decimal import Decimal, ROUND_HALF_UP
from main.models import *
from .services.calculate_values import CalculateValues


class ValuesTitr(models.Model):
    fio = models.ForeignKey(Fio, on_delete=models.DO_NOTHING)
    titrant = models.ForeignKey(Titrant, on_delete=models.DO_NOTHING)
    t_titr = models.DecimalField(max_digits=10, decimal_places=7)
    created_at = models.DateTimeField(auto_now_add=True)
    user_defined_time = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f"{self.t_titr}"



class Values(models.Model):
    fio = models.ForeignKey(Fio, on_delete=models.DO_NOTHING)
    indicator = models.ForeignKey(Indicator, on_delete=models.DO_NOTHING)
    selection_point = models.ForeignKey(Selection_point, on_delete=models.DO_NOTHING)

    replaced_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replacing_values'
    )
    is_replaced = models.BooleanField(default=False)


    # Связь с записью из ValuesTitr
    titrant_value = models.ForeignKey(
        ValuesTitr,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='used_in_values'
    )


    # Возможные варианты повторного ввода:
    REPEAT_CHOICES = [
        ('', 'Не перезаписана'),    # пустая строка – запись не перезаписана
        ('lab', 'Лаборатория'),      # повтор из лаборатории
        ('workshop', 'Цех'),         # повтор из цеха
    ]
    replace_source = models.CharField(
        max_length=10,
        choices=REPEAT_CHOICES,
        blank=True,
        null=True,
        default=''
    )


    # Фиксированные поля для всех возможных показателей
    v_al_ml = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    v_titr_ml = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    ph = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    v_ppa_ml = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    m_f_g = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    m_f_os = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    ph_density = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    t_oc = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    p_gl = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    # Автоматически ставится время создания записи
    created_at = models.DateTimeField(auto_now_add=True)

    # Время, указанное пользователем
    user_defined_time = models.DateTimeField(null=False, blank=False)

    # Расчетные показатели
    v2o5 = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    h2so4 = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    mgso4 = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    susp = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    dry_residue = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    getcontext().prec = 10  # Устанавливаем точность вычислений

    def calculate_values(self):
        """Вычисление расчетных показателей через сервис."""
        results = CalculateValues.calculate_values(self)
        self.v2o5 = results["v2o5"]
        self.h2so4 = results["h2so4"]
        self.mgso4 = results["mgso4"]
        self.susp = results["susp"]
        self.dry_residue = results["dry_residue"]

    def save(self, *args, **kwargs):
        """Перед сохранением пересчитываем расчетные показатели и обновляем статус заменяемой записи."""
        self.calculate_values()

        if self.replaced_by:
            self.replaced_by.is_replaced = True
            self.replaced_by.save(update_fields=['is_replaced'])
            #self.replaced_by.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"

"""
    def calculate_values(self):
        #Вычисление расчетных показателей перед сохранением.
        try:
            # Расчет v2o5 или h2so4 в зависимости от индикатора
            if self.v_al_ml is not None and self.v_titr_ml is not None and self.titrant_value and self.titrant_value.t_titr:
                if self.indicator.indicator_name == "V2O5":  # Если индикатор V2O5
                    self.v2o5 = (self.titrant_value.t_titr * self.v_titr_ml * Decimal(1000)) / self.v_al_ml
                    self.h2so4 = None  # Обнуляем h2so4

                    print(self.titrant_value.t_titr)
                    print(self.v_titr_ml)
                    print(self.v_al_ml)
                    print(self.v2o5)

                    print("ТИТРАНТ", self.titrant_value.titrant, self.titrant_value.t_titr)
                elif self.indicator.indicator_name == "H2SO4":  # Если индикатор H2SO4
                    self.h2so4 = (self.titrant_value.t_titr * self.v_titr_ml * Decimal(1000)) / self.v_al_ml
                    self.v2o5 = None  # Обнуляем v2o5

                    print("ТИТРАНТ", self.titrant_value.titrant, self.titrant_value.t_titr)
                else:
                    self.v2o5 = None
                    self.h2so4 = None
            else:
                self.v2o5 = None
                self.h2so4 = None

            # mgso4 (учитываем два варианта формулы)
            if self.p_gl and self.t_oc and self.ph_density:
                exp_value = (Decimal(0.019) * self.t_oc - Decimal(1.82) * self.ph_density + Decimal(4.09)).exp()
                if Decimal("0.1") < self.p_gl < Decimal("1070"):
                    self.mgso4 = (
                                Decimal("2.057") * self.p_gl + Decimal("0.718") * self.t_oc - Decimal("2070") - Decimal(
                            "1.353") * exp_value)
                elif self.p_gl >= Decimal("1070"):
                    self.mgso4 = (
                                Decimal("2.427") * self.p_gl + Decimal("0.977") * self.t_oc - Decimal("2070") - Decimal(
                            "2471") - Decimal("1.353") * exp_value)
                else:
                    self.mgso4 = None
            else:
                self.mgso4 = None

            # susp
            if self.m_f_os and self.m_f_g and self.v_ppa_ml:
                self.susp = ((self.m_f_os - self.m_f_g) * Decimal(1000)) / self.v_ppa_ml
            else:
                self.susp = None

            # dry
            if self.dry_residue:
                if self.v_titr_ml is not None and self.dry_residue is not None:
                    result = Decimal('1.8') * self.v_titr_ml + Decimal('6.66')
                    self.dry_residue = result.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
                else:
                    self.dry_residue = None
            else:
                self.dry_residue = None

        except Exception as e:
            print(f"Ошибка при вычислении значений: {e}")
"""