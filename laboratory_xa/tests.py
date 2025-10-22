import pytest
from unittest.mock import Mock, patch

from laboratory_xa import analysis_calculations  # путь поправь под свой проект


@pytest.mark.parametrize("func, titr_id, expected_key", [
    (analysis_calculations.calculate_v2o5, 1, "V2O5 %(вычисл)"),
    (analysis_calculations.calculate_v2o5_titr2, 2, "V2O5 %(вычисл)"),
    (analysis_calculations.calculate_h2so4, 5, "H2SO4 %(вычисл)"),
    (analysis_calculations.calculate_caoact, 5, "CaO акт %(вычисл)"),
    (analysis_calculations.calculate_fedisp, 4, "Fe дисп %(вычисл)"),
])
@patch("laboratory_xa.analysis_calculations.ValuesTitrLabXA")
def test_calculations_success(mock_model, func, titr_id, expected_key):
    """Минимальный тест успешного расчёта без реальной базы."""
    # Мокаем запись титра
    mock_record = Mock()
    mock_record.t_titr = 0.5
    mock_model.objects.filter.return_value.select_related.return_value.order_by.return_value.first.return_value = mock_record


    # Подсовываем корректные данные
    fields = {
        "Vт (1), мл": 10.0,
        "Vт (2), мл": 11.0,
        "m нав (1), г": 5.0,
        "m нав (2), г": 5.0,
    }

    result, record = func(fields)

    assert isinstance(result, dict)
    assert expected_key in result
    assert record == mock_record


@patch("laboratory_xa.analysis_calculations.ValuesTitrLabXA")
def test_calculations_missing_field(mock_model):
    """Если нет нужного поля — должна вернуться ошибка."""
    mock_record = Mock()
    mock_record.t_titr = 1.0
    mock_model.objects.filter.return_value.select_related.return_value.order_by.return_value.first.return_value = mock_record


    fields = {"Vт (1), мл": 10.0}

    result, record = analysis_calculations.calculate_v2o5(fields)
    assert "Ошибка" in result
    assert record is None


@patch("laboratory_xa.analysis_calculations.ValuesTitrLabXA")
def test_calculations_no_titr(mock_model):
    """Если титр не найден — возвращает ошибку."""
    mock_model.objects.filter.return_value.select_related.return_value.order_by.return_value.first.return_value = None

    fields = {
        "Vт (1), мл": 10.0,
        "Vт (2), мл": 11.0,
        "m нав (1), г": 5.0,
        "m нав (2), г": 5.0,
    }

    result, record = analysis_calculations.calculate_v2o5(fields)
    assert result == {"Ошибка": "Титр не найден"}
    assert record is None


def test_calculate_mesu_simple():
    """Проверяем простую функцию без ORM."""
    fields = {
        "m тара (1), г": 10,
        "m тара (2), г": 10,
        "m нав (1), г": 20,
        "m нав (2), г": 20,
        "m нав+т (1), г": 25,
        "m нав+т (2), г": 26,
    }

    result, record = analysis_calculations.calculate_mesu(fields)
    assert "W %(вычисл)" in result
    assert record is None
