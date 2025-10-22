import pytest
from decimal import Decimal
from .services.calculate_values import CalculateValues


class Dummy:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.mark.parametrize(
    ('indicator_name,expected_field'),
    [
        ("V2O5", "v2o5"),
        ("H2SO4", "h2so4"),
    ],
)
def test_calculate_values_v2o5_h2so4(indicator_name, expected_field):
    titrant_value = Dummy(t_titr=Decimal("0.07"))
    indicator = Dummy(indicator_name=indicator_name)
    values = Dummy(
        v_al_ml=Decimal("2"),
        v_titr_ml=Decimal("2"),
        titrant_value=titrant_value,
        indicator=indicator,
        p_gl=None, t_oc=None, ph_density=None, m_f_os=None, m_f_g=None, v_ppa_ml=None,
    )
    result = CalculateValues.calculate_values(values)
    expected = (Decimal("0.07") * Decimal("2") * Decimal(1000)) / Decimal("2.0")

    assert result[expected_field] == expected

    for k, v in result.items():
        if k != expected_field:
            assert v is None


def test_calculate_values_mgso4_low_range():
    values = Dummy(
        p_gl=Decimal("500"),
        t_oc=Decimal("10"),
        ph_density=Decimal("1"),
        v_al_ml=None,
        v_titr_ml=None,
        titrant_value=None,
        indicator=None,
        m_f_os=None,
        m_f_g=None,
        v_ppa_ml=None,
    )
    result = CalculateValues.calculate_values(values)

    # Рассчитаем вручную
    exp_value = (Decimal("0.019") * Decimal("10") - Decimal("1.82") * Decimal("1") + Decimal("4.09")).exp()
    expected_mgso4 = Decimal("2.057") * Decimal("500") + Decimal("0.718") * Decimal("10") - Decimal("2070") - Decimal("1.353") * exp_value

    assert result["mgso4"] == expected_mgso4

    for k, v in result.items():
        if k != "mgso4":
            assert v is None


def test_calculate_values_mgso4_high_range():
    values = Dummy(
        p_gl=Decimal("2000"),
        t_oc=Decimal("20"),
        ph_density=Decimal("2"),
        v_al_ml=None,
        v_titr_ml=None,
        titrant_value=None,
        indicator=None,
        m_f_os=None,
        m_f_g=None,
        v_ppa_ml=None,
    )
    result = CalculateValues.calculate_values(values)

    exp_value = (Decimal("0.019") * Decimal("20") - Decimal("1.82") * Decimal("2") + Decimal("4.09")).exp()
    expected_mgso4 = Decimal("2.427") * Decimal("2000") + Decimal("0.977") * Decimal("20") - Decimal("2070") - Decimal("2471") - Decimal("1.353") * exp_value

    assert result["mgso4"] == expected_mgso4

    for k, v in result.items():
        if k != "mgso4":
            assert v is None


def test_calculate_values_susp():
    values = Dummy(
        m_f_os=Decimal("5"),
        m_f_g=Decimal("2"),
        v_ppa_ml=Decimal("1"),
        v_al_ml=None,
        v_titr_ml=None,
        titrant_value=None,
        indicator=None,
        p_gl=None,
        t_oc=None,
        ph_density=None,
    )
    result = CalculateValues.calculate_values(values)

    expected_susp = ((Decimal("5") - Decimal("2")) * Decimal(1000)) / Decimal("1")
    assert result["susp"] == expected_susp

    for k, v in result.items():
        if k != "susp":
            assert v is None


def test_calculate_values_mgso4_high_range():
    values = Dummy(
        p_gl=Decimal("2000"),
        t_oc=Decimal("20"),
        ph_density=Decimal("2"),
        v_al_ml=None,
        v_titr_ml=None,
        titrant_value=None,
        indicator=None,
        m_f_os=None,
        m_f_g=None,
        v_ppa_ml=None,
    )
    result = CalculateValues.calculate_values(values)

    exp_value = (Decimal("0.019") * Decimal("20") - Decimal("1.82") * Decimal("2") + Decimal("4.09")).exp()
    expected_mgso4 = Decimal("2.427") * Decimal("2000") + Decimal("0.977") * Decimal("20") - Decimal("2070") - Decimal("2471") - Decimal("1.353") * exp_value

    assert result["mgso4"] == expected_mgso4

    for k, v in result.items():
        if k != "mgso4":
            assert v is None


def test_calculate_values_susp():
    values = Dummy(
        m_f_os=Decimal("5"),
        m_f_g=Decimal("2"),
        v_ppa_ml=Decimal("1"),
        v_al_ml=None,
        v_titr_ml=None,
        titrant_value=None,
        indicator=None,
        p_gl=None,
        t_oc=None,
        ph_density=None,
    )
    result = CalculateValues.calculate_values(values)

    expected_susp = ((Decimal("5") - Decimal("2")) * Decimal(1000)) / Decimal("1")
    assert result["susp"] == expected_susp

    for k, v in result.items():
        if k != "susp":
            assert v is None


def test_calculate_values_dry_residue():
    values = Dummy(
        v_titr_ml=Decimal("2"),
        dry_residue=True,
        v_al_ml=None,
        titrant_value=None,
        indicator=None,
        p_gl=None,
        t_oc=None,
        ph_density=None,
        m_f_os=None,
        m_f_g=None,
        v_ppa_ml=None,
    )
    result = CalculateValues.calculate_values(values)

    expected_dry_residue = (Decimal("1.8") * Decimal("2") + Decimal("6.66")).quantize(Decimal("0.1"))
    assert result["dry_residue"] == expected_dry_residue

    for k, v in result.items():
        if k != "dry_residue":
            assert v is None