import pytest
from unittest.mock import Mock, patch
from main.services.code_generator import ProbeCodeGenerator

@pytest.fixture
def mock_probe():
    client = Mock()
    client.client = "ОТК"

    selection_point = Mock()
    selection_point.selection_point_name = "Шлак НТМК"

    probe = Mock()
    probe.client = client
    probe.selection_point = selection_point
    return probe


def test_generator_probe_code_with_abb(mock_probe):
    mock_model = Mock()
    mock_model.objects.filter().count.return_value = 5

    result = ProbeCodeGenerator.generate_probe_code(mock_probe, mock_model)

    assert result == "ОТК-ШЛАК-6"


def test_generate_probe_code_without_abbreviation(mock_probe):
    mock_probe.selection_point.selection_point_name = 'Неизвестная точка'

    mock_model = Mock()
    mock_model.objects.filter().count.return_value = 2

    result = ProbeCodeGenerator.generate_probe_code(mock_probe, probes_model=mock_model)

    assert result == 'ОТК-3'


def test_generate_probe_code_for_other_client(mock_probe):
    mock_probe.client.client = 'РМЦ'
    mock_model = Mock()
    mock_model.objects.filter().count.return_value = 7

    result = ProbeCodeGenerator.generate_probe_code(mock_probe, probes_model=mock_model)

    assert result == 'РМЦ-8'