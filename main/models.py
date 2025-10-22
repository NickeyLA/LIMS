from django.db import models
from .services.code_generator import ProbeCodeGenerator


class Laboratory(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Название лаборатории

    def __str__(self):
        return self.name


class Fio(models.Model):
    fio = models.TextField(unique=True)  # Фамилия или ФИО сотрудника
    laboratories = models.ManyToManyField(Laboratory, related_name='fios')  # Уникальный related_name

    def __str__(self):
        return self.fio


class Selection_point(models.Model):
    selection_point_name = models.CharField(max_length=255, unique=True)  # Поле для названия индикатора
    laboratories = models.ManyToManyField(Laboratory, related_name='selection_points')  # Уникальный related_name

    def __str__(self):
        return self.selection_point_name  # Удобное строковое представление объекта


class Titrant(models.Model):
    titrant_name = models.CharField(max_length=266, unique=True)
    laboratories = models.ManyToManyField(Laboratory, related_name='titrants')  # Уникальный related_name

    def __str__(self):
        return self.titrant_name


class Indicator(models.Model):
    indicator_name = models.CharField(max_length=255, unique=True)  # Поле для названия индикатора
    laboratories = models.ManyToManyField(Laboratory, related_name='indicators')  # Уникальный related_name

    def __str__(self):
        return self.indicator_name  # Удобное строковое представление объекта

class Client(models.Model):
    client = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.client


class ProbeIndicator(models.Model):
    probe = models.ForeignKey('Probes', on_delete=models.CASCADE)
    indicator = models.ForeignKey('Indicator', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('probe', 'indicator')


class Probes(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    fio = models.ForeignKey(Fio, on_delete=models.PROTECT)
    selection_point = models.ForeignKey(Selection_point, on_delete=models.PROTECT)
    user_defined_time = models.DateTimeField(null=False, blank=False)
    name_probe = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    comment_for_lab = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    indicators = models.ManyToManyField('Indicator', through='ProbeIndicator')
    code = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id and not self.code:
            self.code = ProbeCodeGenerator.generate_probe_code(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code


class AnalysisResults(models.Model):
    probe_indicator = models.ForeignKey(ProbeIndicator, on_delete=models.PROTECT)
    name_value = models.TextField(blank=False, null=False)
    value = models.TextField(blank=False, null=False)
    fio = models.ForeignKey(Fio, on_delete=models.PROTECT)
    user_defined_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Результат для {self.probe_indicator.probe.code} - {self.probe_indicator.indicator.indicator_name}"
