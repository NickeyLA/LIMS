from django import forms
from main.models import Selection_point, Indicator

class ViewForm(forms.Form):
    selection_point = forms.ModelChoiceField(
        queryset=Selection_point.objects.filter(laboratories__id=2),
        empty_label="Выберите точку отбора",
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_selection_point'})
    )

    indicator = forms.ModelChoiceField(
        queryset=Indicator.objects.all(),
        empty_label="Выберите показатель",
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_indicator'})
    )

    date_from = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'custom-datetime', 'id': 'id_date_from'})
    )

    date_to = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'custom-datetime', 'id': 'id_date_to'})
    )