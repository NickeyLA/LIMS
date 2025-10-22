from django import forms
from .models import ValuesTitrLabXA, Fio, Titrant, AnalysisResults, ProbeIndicator, Probes


class ValuesTitrFormXA(forms.ModelForm):
    fio = forms.ModelChoiceField(
        queryset=Fio.objects.filter(laboratories__id=2),
        empty_label="Выберите ФИО",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_fio_titr'})
    )

    titrant = forms.ModelChoiceField(
        queryset=Titrant.objects.filter(laboratories__id=2).order_by('id'),
        empty_label="Выберите титрант",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_titr'})
    )

    class Meta:
        model = ValuesTitrLabXA  # Указываем новую модель
        fields = [
            'fio', 'titrant', 't_titr', 'v_titr_1', 'v_titr_2', 'v_titr_3', 'v_titr_4', 'used_values', 'user_defined_time'
        ]
        widgets = {
            'user_defined_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'custom-datetime'}),
            't_titr': forms.NumberInput(attrs={'class': 'custom-input', 'value': '0.00'}),
            'v_titr_1': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.01', 'id': 'v_titr_1', 'required': False}),
            'v_titr_2': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.01', 'id': 'v_titr_2', 'required': False}),
            'v_titr_3': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.01', 'id': 'v_titr_3', 'required': False}),
            'v_titr_4': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.01', 'id': 'v_titr_4', 'required': False}),
            'used_values': forms.TextInput(attrs={'class': 'custom-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем начальное значение для used_values, если оно не задано
        if not self.instance.used_values:
            self.initial['used_values'] = '1234'  # По умолчанию используются все значения


class AnalysisResultForm(forms.ModelForm):
    fio = forms.ModelChoiceField(
        queryset=Fio.objects.filter(laboratories__id=2),
        empty_label="Выберите ФИО",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_fio'})
    )

    probe = forms.ModelChoiceField(
        queryset=Probes.objects.order_by('-id')[:20],
        empty_label="Выберите шифр пробы",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_probe'})
    )

    probe_indicator = forms.ModelChoiceField(
        queryset=ProbeIndicator.objects.none(),  # изначально пустой
        empty_label="Выберите показатель",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_probe_indicator'})
    )

    selection_point = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'custom-input',
            'readonly': 'readonly',
            'id': 'id_selection_point',
            'placeholder': 'Точка отбора'
        })
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'probe' in self.data:
            try:
                probe_id = int(self.data.get('probe'))
                self.fields['probe_indicator'].queryset = ProbeIndicator.objects.filter(probe_id=probe_id)
            except (ValueError, TypeError):
                self.fields['probe_indicator'].queryset = ProbeIndicator.objects.none()
        elif self.instance.pk:
            # Если это редактирование, заполнить на основе instance
            self.fields['probe_indicator'].queryset = ProbeIndicator.objects.filter(probe=self.instance.probe)

    class Meta:
        model = AnalysisResults
        fields = ['probe', 'probe_indicator', 'value', 'name_value', 'fio', 'user_defined_time']
        widgets = {
            'user_defined_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'custom-datetime',
                                                            'id': 'id_analys_user_defined_time', 'readonly': 'readonly'}),
            'value': forms.TextInput(attrs={'class': 'custom-input'}),
            'name_value': forms.TextInput(attrs={'class': 'custom-input'}),
        }

