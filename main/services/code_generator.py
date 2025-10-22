from django.apps import apps


class ProbeCodeGenerator:
    SELECTION_POINT_ABBREVIATIONS = {
        'Кислота серная (в.к.)': 'КС',
        'Известь (в.к.)': 'ИЗВТЬ',
        'Шихта на обжиг': 'ШНО',
        'Шихта обожженная': 'ШО',
        'Шлам отвальный': 'КЖС',
        'Зашлакованность': 'ЗАШЛ',
        'Феррованадий': 'FeV',
        'Пентоксид ванадия': 'V2O5',
        'Шлак НТМК': 'ШЛАК',
        'Алюминий': 'Al',
        'Известняк': 'ИЗВК',
        'Сливной шлак': 'СЛШ',
    }

    @staticmethod
    def generate_probe_code(probe, probes_model=None):
        if probes_model is None:
            probes_model = apps.get_model('main', 'Probes')
        client_name = probe.client.client.upper()

        if client_name == 'ОТК':
            abbreviation = ProbeCodeGenerator.SELECTION_POINT_ABBREVIATIONS.get(
                probe.selection_point.selection_point_name)
            if abbreviation:
                client_selection_point_count = probes_model.objects.filter(
                    client=probe.client,
                    selection_point=probe.selection_point
                ).count()
                return f"{probe.client.client}-{abbreviation}-{client_selection_point_count + 1}"
            else:
                client_count = probes_model.objects.filter(client=probe.client).count()
                return f"{probe.client.client}-{client_count + 1}"
        else:
            client_count = probes_model.objects.filter(client=probe.client).count()
            return f"{probe.client.client}-{client_count + 1}"
