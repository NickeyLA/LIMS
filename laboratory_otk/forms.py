from django import forms
from main.models import Probes, Client, Selection_point, Fio, Indicator

class ProbForm(forms.ModelForm):
    RSA_COMMENT_ELEMENTS_LIST = [
        'V2O5 (РСА)', 'Fe общ', 'CaO общ', 'CaO ввод', 'TiO2', 'MnO',
        'Al2O3', 'SiO2', 'MgO', 'Cr2O3', 'CaCO3', 'CaO+MgO', 'Fe2O3', 'FeO',
        'H2O', 'ZnO', 'CaO ввод. mod', 'CaO общ. mod', 'М (общ.)', 'М (ввод.)'
    ]
    AES_ISP_COMMENT_ELEMENTS_LIST = [
        'V2O5 (АЭС ИСП)', 'Fe', 'As', 'K', 'Ca', 'Al', 'Ni', 'Pb', 'P', 'Si', 'Cu',
        'SO4', 'Ti', 'Mg', 'Zr', 'V', 'Cr', 'Mo', 'Zn', 'Mn', 'W', 'Na'
    ]
    INDICATOR_GROUPS = {
        'Мокрая химия': [
            'V2O5', 'Fe дисп', 'V2O5 k/r', 'CaO акт', 'V2O5 pH', 'SO4', 'V2O5 в/р', 'H2SO4'
        ],
        'РСА': [
            'РСА'
        ],
        'АЭС ИСП': [
            'АЭС ИСП'
        ],
        'C, S анализатор': ['C', 'S'],
        'Физ-мех испытания': ['органолептика', 'плотность', 'ППП', 'шлак'],
        'ОТК': [
            'определение марки', '№ плавки', 'вес', 'кол-во мест', '№ партии', 'кол-во биг-бегов', '№ короба',
            'примечание', 'процент', '№ места', 'поставщик', 'основной элемент', 'машина/вагон', 'грансостав',
            'пылевидные и глинистые включения', 'глина в комках', 'М/в', 'влага', '№ вагона', 'органолептика', 'фракция'
        ],
    }

    indicators = forms.ModelMultipleChoiceField(
        queryset=Indicator.objects.all().order_by('indicator_name'),  # Сортируем по имени
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}),  # Добавляем класс для стилей
        required=False,
        label='Выберите показатели для анализа'
    )

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        empty_label="Выберите заказчика",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_fio'})
    )

    fio = forms.ModelChoiceField(
        queryset=Fio.objects.filter(laboratories__id=3),
        empty_label="Выберите ФИО",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_fio'})
    )

    selection_point = forms.ModelChoiceField(
        queryset=Selection_point.objects.filter(laboratories__id=3),
        empty_label="Выберите точку отбора",
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'id_selection_point'})
    )

    class Meta:
        model = Probes  # Указываем модель, на основе которой создается форма
        fields = '__all__'  # Указываем, какие поля модели должны быть в форме
        widgets = {
            'user_defined_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'custom-datetime', 'id': 'id_us_def_time'}),
            'comment': forms.HiddenInput(attrs={'id': 'id_comment'}),
            'comment_for_lab': forms.TextInput(attrs={'class': 'custom-input', 'id': 'id_comment_for_lab'}),
            'name_probe': forms.TextInput(attrs={'class': 'custom-input', 'id': 'id_name_probe'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indicator_groups = self.INDICATOR_GROUPS
        self.fields['rsa_comment_elements'] = forms.MultipleChoiceField(
            choices=[(el, el) for el in self.RSA_COMMENT_ELEMENTS_LIST],
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}),
            required=False,
            label='Показатели РСА (ручной ввод)'
        )
        self.fields['aes_isp_elements_for_comment'] = forms.MultipleChoiceField(
            choices=[(el, el) for el in self.AES_ISP_COMMENT_ELEMENTS_LIST],
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}),
            required=False,
            label='Показатели АЭС ИСП (ручной ввод)'
        )
