# viewer_gmc/forms.py
from django import forms
from main.models import Selection_point, Indicator
from laboratory_gmc.models import Values

class ViewFormGMC(forms.Form):
    indicator = forms.ModelChoiceField(
        queryset=Indicator.objects.all(),
        empty_label="Выберите показатель",
        required=False,
        widget=forms.Select(
            attrs={'class': 'custom-select', 'id': 'id_indicator'})
    )

    selection_point = forms.ModelChoiceField(
        queryset=Selection_point.objects.filter(laboratories__id=1),
        empty_label="Выберите точку отбора",
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_selection_point'})
    )

    replaced_by = forms.ModelChoiceField(
        queryset=Values.objects.all().order_by('-id'),
        required=False,
        empty_label="Выберите заменяемую запись",
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_replaced_by'})
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