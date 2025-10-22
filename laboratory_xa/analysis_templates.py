ANALYSIS_TEMPLATES = {
    ("H2SO4", "Кислота серная (в.к.)"): {
        "fields": [
            {"name": "m нав (1), г", "value": "", "editable": True},
            {"name": "m нав (2), г", "value": "", "editable": True},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_h2so4"
    },

    ("органолептика", "Кислота серная (в.к.)"): {
        "fields": [
            {"name": "цвет", "value": "", "editable": True},
            {"name": "органика", "value": "", "editable": True},
            {"name": "запах", "value": "", "editable": True},
            {"name": "примеси", "value": "", "editable": True}
        ],
        "formula": ""
    },

    ("CaO акт", "Известь (в.к.)"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.2500", "editable": False},
            {"name": "m нав (2), г", "value": "0.2500", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_caoact"
    },

    ("V2O5", "Шихта на обжиг"): {
        "fields": [
            {"name": "m нав (1), г", "value": "", "editable": True},
            {"name": "m нав (2), г", "value": "", "editable": True},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("Fe дисп", "Шихта на обжиг"): {
        "fields": [
            {"name": "m нав (1), г", "value": "1.0000", "editable": False},
            {"name": "m нав (2), г", "value": "1.0000", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_fedisp"
    },


    ("V2O5", "Шихта обожженная"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.5000", "editable": False},
            {"name": "m нав (2), г", "value": "0.5000", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("V2O5 k/r", "Шихта обожженная"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.5000", "editable": False},
            {"name": "m нав (2), г", "value": "0.5000", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("V2O5 k/r", "Шлам отвальный"): {
        "fields": [
            {"name": "m нав (1), г", "value": "1.0000", "editable": False},
            {"name": "m нав (2), г", "value": "1.0000", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5_titr2"
    },

    ("V2O5 pH", "Шихта обожженная"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.5000", "editable": False},
            {"name": "m нав (2), г", "value": "0.5000", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("V2O5", "Шлам отвальный"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.2500", "editable": False},
            {"name": "m нав (2), г", "value": "0.2500", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("V2O5 к/р", "Шлам отвальный"): {
        "fields": [
            {"name": "m нав (1), г", "value": "1", "editable": False},
            {"name": "m нав (2), г", "value": "1", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5_titr2"
    },

    ("V2O5", "Кек 5 реактора"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.2500", "editable": False},
            {"name": "m нав (2), г", "value": "0.2500", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("V2O5 к/р", "Кек 5 реактора"): {
        "fields": [
            {"name": "m нав (1), г", "value": "1", "editable": False},
            {"name": "m нав (2), г", "value": "1", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5_titr2"
    },

    ("влага", "Металлопродукт"): {
        "fields": [
            {"name": "влага", "value": "", "editable": True}
        ],
        "formula": ""
    },

    ("V2O5", "Конвейер 18а"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.2500", "editable": False},
            {"name": "m нав (2), г", "value": "0.2500", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("влага", "Конвейер 18а"): {
        "fields": [
            {"name": "влага", "value": "", "editable": True}
        ],
        "formula": ""
    },

    ("V", "FeV80 (паспорт)"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.1000", "editable": False},
            {"name": "m нав (2), г", "value": "0.1000", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("грансостав", "Алюминий (исследов)"): {
        "fields": [
            {"name": "+3,15", "value": "", "editable": True},
            {"name": "+1", "value": "", "editable": True},
            {"name": "-1", "value": "", "editable": True},
            {"name": "+0,5", "value": "", "editable": True},
            {"name": "+0,2", "value": "", "editable": True},
            {"name": "+0,1", "value": "", "editable": True},
            {"name": "Рассев %(вычисл)", "value": "", "editable": True}
        ],
        "formula": ""
    },

    ("грансостав", "Рассев шихты с классификаторов"): {
        "fields": [
            {"name": "1, -0,063", "value": "", "editable": True},
            {"name": "2, -0,063", "value": "", "editable": True},
            {"name": "3, -0,063", "value": "", "editable": True},
            {"name": "Рассев %(вычисл)", "value": "", "editable": True}
        ],
        "formula": ""
    },

    ("грансостав", "Шихта на обжиг"): {
        "fields": [
            {"name": "+0,2", "value": "", "editable": True},
            {"name": "+0,16", "value": "", "editable": True},
            {"name": "+0,1", "value": "", "editable": True},
            {"name": "+0,063", "value": "", "editable": True},
            {"name": "-0,063", "value": "", "editable": True},
            {"name": "Рассев %(вычисл)", "value": "", "editable": True}
        ],
        "formula": ""
    },

    ("грансостав", "Шихта обожженная"): {
        "fields": [
            {"name": "+0,2", "value": "", "editable": True},
            {"name": "+0,16", "value": "", "editable": True},
            {"name": "+0,1", "value": "", "editable": True},
            {"name": "+0,063", "value": "", "editable": True},
            {"name": "-0,063", "value": "", "editable": True},
            {"name": "Рассев %(вычисл)", "value": "", "editable": True}
        ],
        "formula": ""
    },

    ("грансостав", "Шлам отвальный СС"): {
        "fields": [
            {"name": "+0,2", "value": "", "editable": True},
            {"name": "+0,16", "value": "", "editable": True},
            {"name": "+0,1", "value": "", "editable": True},
            {"name": "+0,063", "value": "", "editable": True},
            {"name": "+0,063", "value": "", "editable": True},
            {"name": "Рассев %(вычисл)", "value": "", "editable": True}
        ],
        "formula": ""
    },

    ("V2O5 pH", "СОП 78-2021"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.5000", "editable": False},
            {"name": "m нав (2), г", "value": "0.5000", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("V2O5 pH", "СОП 75-2021"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.5000", "editable": False},
            {"name": "m нав (2), г", "value": "0.5000", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("V2O5 к/р", "СОП 6-2017Д"): {
        "fields": [
            {"name": "m нав (1), г", "value": "1", "editable": False},
            {"name": "m нав (2), г", "value": "1", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5_titr2"
    },

    ("V2O5 к/р", "СОП 07-2022"): {
        "fields": [
            {"name": "m нав (1), г", "value": "1", "editable": False},
            {"name": "m нав (2), г", "value": "1", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5_titr2"
    },

    ("V2O5 к/р", "СОП 67-2022"): {
        "fields": [
            {"name": "m нав (1), г", "value": "1", "editable": False},
            {"name": "m нав (2), г", "value": "1", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5_titr2"
    },

    ("V2O5 к/р", "СОП 08-2022"): {
        "fields": [
            {"name": "m нав (1), г", "value": "1", "editable": False},
            {"name": "m нав (2), г", "value": "1", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5_titr2"
    },

    ("V2O5 к/р", "СОП 82-2021"): {
        "fields": [
            {"name": "m нав (1), г", "value": "1", "editable": False},
            {"name": "m нав (2), г", "value": "1", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5_titr2"
    },

    ("V2O5", "СОП 93-2025"): {
        "fields": [
            {"name": "m нав (1), г", "value": "", "editable": True},
            {"name": "m нав (2), г", "value": "", "editable": True},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_v2o5"
    },

    ("CaO акт", "81-2018Д"): {
        "fields": [
            {"name": "m нав (1), г", "value": "0.2500", "editable": False},
            {"name": "m нав (2), г", "value": "0.2500", "editable": False},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_caoact"
    },

    ("H2SO4", "КО 25-2024"): {
        "fields": [
            {"name": "m нав (1), г", "value": "", "editable": True},
            {"name": "m нав (2), г", "value": "", "editable": True},
            {"name": "Vт (1), мл", "value": "", "editable": True},
            {"name": "Vт (2), мл", "value": "", "editable": True}
        ],
        "formula": "calculate_h2so4"
    },

}


