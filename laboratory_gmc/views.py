import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ValuesForm, ValuesTitrForm
from .models import Values, ValuesTitr


logger = logging.getLogger(__name__)

def lab_page(request):
    form = ValuesForm()
    titrant_form = ValuesTitrForm()

    if request.method == 'POST':
        # Если пришла форма для титранта
        if request.POST.get('form_type') == 'titrant_form':
            titrant_form = ValuesTitrForm(request.POST)
            if titrant_form.is_valid():
                titrant_form.save()
                logger.info("ValuesTitr saved")
                return redirect('lab_page')
            else:
                logger.warning("Titrant form invalid: %s", titrant_form.errors)

        # Иначе — основная форма Values
        else:
            # Сделаем копию POST, чтобы было mutable (на случай, если нужно править поля)
            post = request.POST.copy()

            form = ValuesForm(post)
            if form.is_valid():
                instance = form.save(commit=False)

                # Получаем titrant из скрытого поля (в шаблоне это 'titrant_value_hidden')
                titrant_value_id = request.POST.get('titrant_value_hidden')
                if titrant_value_id:
                    try:
                        titrant_value = ValuesTitr.objects.get(pk=int(titrant_value_id))
                        instance.titrant_value = titrant_value
                    except (ValuesTitr.DoesNotExist, ValueError):
                        instance.titrant_value = None

                # Сохраняем новую запись
                instance.save()
                logger.info("Values instance saved: id=%s, replaced_by=%s", instance.id, instance.replaced_by_id)

                # Теперь пометим старую запись (если была выбрана) как is_replaced=True
                if instance.replaced_by_id:
                    Values.objects.filter(pk=instance.replaced_by_id).update(is_replaced=True)
                    logger.info("Old record %s marked as replaced", instance.replaced_by_id)

                return redirect('lab_page')
            else:
                # Логируем ошибки и POST для отладки
                logger.warning("ValuesForm invalid: %s", form.errors)
                logger.debug("POST data: %s", dict(request.POST))

    # GET или невалидный POST — формируем контекст
    values_list = Values.objects.filter(is_replaced=False).select_related(
        'fio', 'selection_point', 'indicator', 'replaced_by', 'titrant_value'
    ).order_by('-created_at')[:1000]

    # Для PostgreSQL: distinct('titrant') — возвращаем по каждому titrant последний
    try:
        titrant_list = ValuesTitr.objects.order_by('titrant', '-created_at').distinct('titrant')
    except Exception:
        # На случай другой БД — fallback: просто берем последние 200
        titrant_list = ValuesTitr.objects.order_by('-created_at')[:200]

    last_entry = ValuesTitr.objects.order_by('-created_at').first()

    context = {
        'form': form,
        'titrant_form': titrant_form,
        'values_list': values_list,
        'titrant_list': titrant_list,
        'last_fio_titr': last_entry.fio.id if last_entry else None,
    }
    # views.py, перед render
    form.fields['replaced_by'].queryset = Values.objects.filter(is_replaced=False).order_by('-id')[:100]

    return render(request, 'laboratory_gmc/index.html', context)


def get_record_data(request, record_id):
    try:
        record = Values.objects.get(id=record_id)
        data = {
            'id': record.id,
            'fio': record.fio.id,
            'selection_point': record.selection_point.id,
            'user_defined_time': record.user_defined_time.strftime('%Y-%m-%dT%H:%M'),
            'v_titr_ml': str(record.v_titr_ml) if record.v_titr_ml is not None else '',
            'v_al_ml': str(record.v_al_ml) if record.v_al_ml is not None else '',
            'ph': str(record.ph) if record.ph is not None else '',
            'v_ppa_ml': str(record.v_ppa_ml) if record.v_ppa_ml is not None else '',
            'm_f_g': str(record.m_f_g) if record.m_f_g is not None else '',
            'm_f_os': str(record.m_f_os) if record.m_f_os is not None else '',
            'ph_density': str(record.ph_density) if record.ph_density is not None else '',
            't_oc': str(record.t_oc) if record.t_oc is not None else '',
            'p_gl': str(record.p_gl) if record.p_gl is not None else '',
            'replaced_by': record.replaced_by_id,
            'replace_source': record.replace_source
        }
        return JsonResponse(data)
    except Values.DoesNotExist:
        return JsonResponse({'error': 'Record not found'}, status=404)
