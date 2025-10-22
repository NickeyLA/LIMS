from decimal import Decimal
from .models import ValuesTitrLabXA

def calculate_v2o5(fields: dict) -> tuple[dict, None]:
    titr_record = (
        ValuesTitrLabXA.objects
        .filter(titrant_id=1)
        .select_related('titrant')
        .order_by('-created_at')
        .first()
    )
    if titr_record is None:
        return {"Ошибка": "Титр не найден"}, None

    T = float(titr_record.t_titr)

    required_fields = ["Vт (1), мл", "Vт (2), мл", "m нав (1), г", "m нав (2), г"]
    for field in required_fields:
        if field not in fields:
            return {"Ошибка": f"Отсутствует поле: {field}"}, None
        if not isinstance(fields[field], (int, float)):
            return {"Ошибка": f"Поле {field} должно быть числом, получено: {fields[field]}"}, None

    try:
        Vt1 = float(fields["Vт (1), мл"])
        Vt2 = float(fields["Vт (2), мл"])
        m1 = float(fields["m нав (1), г"])
        m2 = float(fields["m нав (2), г"])
    except ValueError as e:
        return {"Ошибка": f"Некорректные числовые значения: {str(e)}"}, None

    try:
        v2o5_1 = (T * Vt1 * 100) / m1
        v2o5_2 = (T * Vt2 * 100) / m2
        result = (v2o5_1 + v2o5_2) / 2
    except ZeroDivisionError:
        return {"Ошибка": "Деление на ноль при расчёте"}, None

    return {"V2O5 %(вычисл)": round(result, 5)}, titr_record


def calculate_v2o5_titr2(fields: dict) -> tuple[dict, None]:
    titr_record = (
        ValuesTitrLabXA.objects
        .filter(titrant_id=1)
        .select_related('titrant')
        .order_by('-created_at')
        .first()
    )
    if titr_record is None:
        return {"Ошибка": "Титр не найден"}, None

    T = float(titr_record.t_titr)

    required_fields = ["Vт (1), мл", "Vт (2), мл", "m нав (1), г", "m нав (2), г"]
    for field in required_fields:
        if field not in fields:
            return {"Ошибка": f"Отсутствует поле: {field}"}, None
        if not isinstance(fields[field], (int, float)):
            return {"Ошибка": f"Поле {field} должно быть числом, получено: {fields[field]}"}, None

    try:
        Vt1 = float(fields["Vт (1), мл"])
        Vt2 = float(fields["Vт (2), мл"])
        m1 = float(fields["m нав (1), г"])
        m2 = float(fields["m нав (2), г"])
    except ValueError as e:
        return {"Ошибка": f"Некорректные числовые значения: {str(e)}"}, None

    try:
        v2o5_1 = (T * Vt1 * 100) / m1
        v2o5_2 = (T * Vt2 * 100) / m2
        result = (v2o5_1 + v2o5_2) / 2
    except ZeroDivisionError:
        return {"Ошибка": "Деление на ноль при расчёте"}, None

    return {"V2O5 %(вычисл)": round(result, 5)}, titr_record


def calculate_h2so4(fields: dict) -> tuple[dict, None]:
    titr_record = (
        ValuesTitrLabXA.objects
        .filter(titrant_id=1)
        .select_related('titrant')
        .order_by('-created_at')
        .first()
    )
    if titr_record is None:
        return {"Ошибка": "Титр не найден"}, None

    T = float(titr_record.t_titr)

    required_fields = ["Vт (1), мл", "Vт (2), мл", "m нав (1), г", "m нав (2), г"]
    for field in required_fields:
        if field not in fields:
            return {"Ошибка": f"Отсутствует поле: {field}"}, None
        if not isinstance(fields[field], (int, float)):
            return {"Ошибка": f"Поле {field} должно быть числом, получено: {fields[field]}"}, None

    try:
        Vt1 = float(fields["Vт (1), мл"])
        Vt2 = float(fields["Vт (2), мл"])
        m1 = float(fields["m нав (1), г"])
        m2 = float(fields["m нав (2), г"])
    except ValueError as e:
        return {"Ошибка": f"Некорректные числовые значения: {str(e)}"}, None

    try:
        res1 = (T * Vt1 * 100) / m1
        res2 = (T * Vt2 * 100) / m2
        result = (res1 + res2) / 2
    except ZeroDivisionError:
        return {"Ошибка": "Деление на ноль при расчёте"}, None

    if abs(res1 - res2) > 0.6925:
        key = "H2SO4 %(вычисл)"
    else:
        key = "H2SO4 %(вычисл) ПОВТОРИТЬ"

    return {key: round(result, 5)}, titr_record


def calculate_caoact(fields: dict) -> tuple[dict, None]:
    titr_record = (
        ValuesTitrLabXA.objects
        .filter(titrant_id=1)
        .select_related('titrant')
        .order_by('-created_at')
        .first()
    )
    if titr_record is None:
        return {"Ошибка": "Титр не найден"}, None

    T = float(titr_record.t_titr)

    required_fields = ["Vт (1), мл", "Vт (2), мл", "m нав (1), г", "m нав (2), г"]
    for field in required_fields:
        if field not in fields:
            return {"Ошибка": f"Отсутствует поле: {field}"}, None
        if not isinstance(fields[field], (int, float)):
            return {"Ошибка": f"Поле {field} должно быть числом, получено: {fields[field]}"}, None

    try:
        Vt1 = float(fields["Vт (1), мл"])
        Vt2 = float(fields["Vт (2), мл"])
        m1 = float(fields["m нав (1), г"])
        m2 = float(fields["m нав (2), г"])
    except ValueError as e:
        return {"Ошибка": f"Некорректные числовые значения: {str(e)}"}, None

    try:
        res1 = (T * Vt1 * 100) / m1
        res2 = (T * Vt2 * 100) / m2
        result = (res1 + res2) / 2
    except ZeroDivisionError:
        return {"Ошибка": "Деление на ноль при расчёте"}, None

    if abs(res1 - res2) > 0.9:
        key = "CaO акт %(вычисл)"
    else:
        key = "CaO акт %(вычисл) ПОВТОРИТЬ"

    return {key: round(result, 5)}, titr_record


def calculate_fedisp(fields: dict) -> tuple[dict, None]:
    titr_record = (
        ValuesTitrLabXA.objects
        .filter(titrant_id=1)
        .select_related('titrant')
        .order_by('-created_at')
        .first()
    )
    if titr_record is None:
        return {"Ошибка": "Титр не найден"}, None

    T = float(titr_record.t_titr)

    required_fields = ["Vт (1), мл", "Vт (2), мл", "m нав (1), г", "m нав (2), г"]
    for field in required_fields:
        if field not in fields:
            return {"Ошибка": f"Отсутствует поле: {field}"}, None
        if not isinstance(fields[field], (int, float)):
            return {"Ошибка": f"Поле {field} должно быть числом, получено: {fields[field]}"}, None

    try:
        Vt1 = float(fields["Vт (1), мл"])
        Vt2 = float(fields["Vт (2), мл"])
        m1 = float(fields["m нав (1), г"])
        m2 = float(fields["m нав (2), г"])
    except ValueError as e:
        return {"Ошибка": f"Некорректные числовые значения: {str(e)}"}, None

    try:
        res1 = (T * Vt1 * 100) / m1
        res2 = (T * Vt2 * 100) / m2
        result = (res1 + res2) / 2
    except ZeroDivisionError:
        return {"Ошибка": "Деление на ноль при расчёте"}, None

    return {"Fe дисп %(вычисл)": round(result, 5)}, titr_record


def calculate_mesu(fields: dict) -> tuple[dict, None]:
    required_fields = ["m тара (1), г", "m тара (2), г", "m нав (1), г", "m нав (2), г", "m нав+т (1), г", "m нав+т (2), г"]
    for field in required_fields:
        if field not in fields:
            return {"Ошибка": f"Отсутствует поле: {field}"}, None
        if not isinstance(fields[field], (int, float)):
            return {"Ошибка": f"Поле {field} должно быть числом, получено: {fields[field]}"}, None

    try:
        mta1 = float(fields["m тара (1), г"])
        mta2 = float(fields["m тара (2), г"])
        mnav1 = float(fields["m нав (1), г"])
        mnav2 = float(fields["m нав (2), г"])
        mnavt1 = float(fields["m нав+т (1), г"])
        mnavt2 = float(fields["m нав+т (2), г"])
    except ValueError as e:
        return {"Ошибка": f"Некорректные числовые значения: {str(e)}"}, None

    try:
        res1 = (mnav1 - (mnavt1 - mta1)) * 100 / mnav1
        res2 = (mnav2 - (mnavt2 - mta2)) * 100 / mnav2
        result = (res1 + res2) / 2
    except ZeroDivisionError:
        return {"Ошибка": "Деление на ноль при расчёте"}, None

    return {"W %(вычисл)": round(result, 5)}, None