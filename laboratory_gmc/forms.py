from django import forms
from laboratory_gmc.models import *
from main.models import *

class ValuesForm(forms.ModelForm):
    user_defined_time = forms.DateTimeField(
        input_formats=[
            '%Y-%m-%dT%H:%M',        # формат от input[type=datetime-local]
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
        ],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'custom-datetime',
            'id': 'id_us_def_time'
        })
    )

    fio = forms.ModelChoiceField(
        queryset=Fio.objects.filter(laboratories__id=1),
        empty_label="Выберите ФИО",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_fio'})
    )

    indicator = forms.ModelChoiceField(
        queryset=Indicator.objects.all(),
        empty_label="Выберите показатель",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_indicator', 'style': 'pointer-events: none;'})
    )

    selection_point = forms.ModelChoiceField(
        queryset=Selection_point.objects.filter(laboratories__id=1),
        empty_label="Выберите точку отбора",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_selection_point'})
    )

    # forms.py
    replaced_by = forms.ModelChoiceField(
        queryset=Values.objects.all().order_by('-id'),  # без среза
        required=False,
        empty_label="Выберите заменяемую запись",
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_replaced_by'})
    )


    class Meta:
        model = Values
        fields = [
            'fio', 'indicator', 'selection_point', 'replaced_by',
            'replace_source', 'v_al_ml', 'v_titr_ml', 'ph',
            'v_ppa_ml', 'm_f_g', 'm_f_os',
            'ph_density', 't_oc', 'p_gl', 'user_defined_time',
            'v2o5', 'h2so4', 'mgso4', 'susp', 'dry_residue'
        ]
        widgets = {
            'v_al_ml': forms.NumberInput(attrs={'class': 'custom-input', 'id': 'id_v_al_ml', 'readonly': 'readonly'}),
            'v_titr_ml': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.0001', 'id': 'id_v_titr_ml'}),
            'ph': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.0001', 'id': 'id_ph'}),
            'v_ppa_ml': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.0001', 'id': 'id_v_ppa_ml'}),
            'm_f_g': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.0001', 'id': 'id_m_f_g'}),
            'm_f_os': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.0001', 'id': 'id_m_f_os'}),
            'ph_density': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.0001'}),
            't_oc': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.0001', 'id': 'id_t_oc'}),
            'p_gl': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.0001', 'id': 'id_p_gl'}),
            'v2o5': forms.NumberInput(attrs={'class': 'custom-input', 'id': 'id_v2o5', 'readonly': 'readonly'}),
            'h2so4': forms.NumberInput(attrs={'class': 'custom-input', 'id': 'id_h2so4', 'readonly': 'readonly'}),
            'mgso4': forms.NumberInput(attrs={'class': 'custom-input', 'id': 'id_mgso4', 'readonly': 'readonly'}),
            'susp': forms.NumberInput(attrs={'class': 'custom-input', 'id': 'id_susp', 'readonly': 'readonly'}),
            'dry_residue': forms.NumberInput(attrs={'class': 'custom-input', 'id': 'id_dry_residue', 'readonly': 'readonly'}),
        }

class ValuesTitrForm(forms.ModelForm):
    fio = forms.ModelChoiceField(
        queryset=Fio.objects.filter(laboratories__id=1),
        empty_label="Выберите ФИО",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_fio_titr'})
    )

    titrant = forms.ModelChoiceField(
        queryset=Titrant.objects.filter(laboratories__id=1).order_by('id'),
        empty_label="Выберите титрант",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_titr'})
    )

    class Meta:
        model = ValuesTitr
        fields = ['fio', 'titrant', 't_titr', 'user_defined_time']
        widgets = {
            'user_defined_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'custom-datetime'}),
            't_titr': forms.NumberInput(attrs={'class': 'custom-input', 'value': '0.00'}),
        }
