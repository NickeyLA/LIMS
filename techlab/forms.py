from django import forms
from main.models import Selection_point


class TechlabForm(forms.Form):
    selection_point = forms.ModelChoiceField(
        queryset=Selection_point.objects.filter(laboratories__id=1),
        empty_label="Выберите точку отбора",
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_selection_point'})
    )

    date_from = forms.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'custom-datetime',
            'id': 'id_date_from'
        })
    )

    date_to = forms.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'custom-datetime',
            'id': 'id_date_to'
        })
    )


    # Список показателей
    INDICATOR_FIELDS = [
        ("v2o5", "V2O5"),
        ("h2so4", "H2SO4"),
        ("mgso4", "MgSO4"),
        ("susp", "Взвесь"),
        ("dry_residue", "Усл. сух. ост."),
        ("ph_density", "pH"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Для каждой точки отбора создаём отдельное поле с чекбоксами
        for point in Selection_point.objects.filter(laboratories__id=1).order_by("selection_point_name"):
            field_name = f"indicators_point_{point.id}"
            self.fields[field_name] = forms.MultipleChoiceField(
                choices=self.INDICATOR_FIELDS,
                widget=forms.CheckboxSelectMultiple(attrs={"class": "checkbox"}),
                required=False,
                label=f"{point.selection_point_name}"
            )