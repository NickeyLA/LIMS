const probes = {
    "4 мешалка": {indicator: "V2O5", v_al_ml: 2, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph']},
    "1 реактор": {indicator: "V2O5", v_al_ml: 2, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph']},
    "2 реактор": {indicator: "V2O5", v_al_ml: 2, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph']},
    "3 реактор": {indicator: "V2O5", v_al_ml: 2, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph']},
    "4 реактор": {indicator: "V2O5", v_al_ml: 2, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph']},
    "5 реактор": {indicator: "V2O5", v_al_ml: 2, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph']},
    "Насосная": {indicator: "pH", v_al_ml: null, titrant: '', fields: ['ph']},
    "Газоочистка": {indicator: "pH", v_al_ml: null, titrant: '', fields: ['ph']},
    "Бак 4/6": {indicator: "V2O5", v_al_ml: 2, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph', 'v_ppa_ml', 'm_f_g', 'm_f_os']},
    "Бак 4/7": {indicator: "V2O5", v_al_ml: 5, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph']},
    "Бак 1": {indicator: "V2O5", v_al_ml: 5, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph', 'v_ppa_ml', 'm_f_g', 'm_f_os']},
    "Бак 2": {indicator: "V2O5", v_al_ml: 5, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph', 'v_ppa_ml', 'm_f_g', 'm_f_os']},
    "Верхний слив 9м сгустителя": {indicator: "V2O5", v_al_ml: 25, titrant: 'Соль Мора 0,04 моль/л', fields: ['v_titr_ml', 'ph']},
    "Бак репульпации": {indicator: "V2O5", v_al_ml: 25, titrant: 'Соль Мора 0,04 моль/л', fields: ['v_titr_ml', 'ph']},
    "Бак 4/9": {indicator: "pH", v_al_ml: null, titrant: '', fields: ['ph', 'ph_density', 't_oc', 'p_gl']},
    "Бак 4/10": {indicator: "H2SO4", v_al_ml: 5, titrant: 'NaOH 0,6 моль/л', fields: ['v_titr_ml', 'ph']},
    "Смеситель 1": {indicator: "pH", v_al_ml: null, titrant: '', fields: ['ph']},
    "Смеситель 1А": {indicator: "V2O5", v_al_ml: 2, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph']},
    "Сгуститель": {indicator: "V2O5", v_al_ml: 25, titrant: 'Соль Мора 0,04 моль/л', fields: ['v_titr_ml', 'ph']},
    "5 реактор ТЛ": {indicator: "V2O5", v_al_ml: 2, titrant: 'Соль Мора 0,07 моль/л', fields: ['v_titr_ml', 'ph']},
    "Желоб 3 реактора": {indicator: "pH", v_al_ml: null, titrant: '', fields: ['ph']},
    "Бак 309": {indicator: "Усл. сух. ост.", v_al_ml: 2, titrant: '', fields: ['v_titr_ml', 'ph']},
    "8 перколятор": {indicator: "Усл. сух. ост.", v_al_ml: 2, titrant: '', fields: ['v_titr_ml', 'ph']},
    "Титаник": {indicator: "pH", v_al_ml: null, titrant: '', fields: ['ph']}
};


document.addEventListener('DOMContentLoaded', function () {
    const fioData = document.getElementById('fio-data');
    const fioDataTitr = document.getElementById('fio-data-titr')

    const lastFio = fioData.dataset.lastFio;
    const lastFioTitr = fioDataTitr.dataset.lastFioTitr;

    const fioField = document.querySelector('[id="id_fio"]');
    const fioFieldTitr = document.querySelector('[id="id_fio_titr"]');

    if (lastFio && fioField) {
        fioField.value = lastFio;
    }
    if (lastFioTitr && fioFieldTitr) {
        fioFieldTitr.value = lastFioTitr;
    }

    const selectionPoint = document.querySelector('[id="id_selection_point"]');
    const indicatorField = document.querySelector('[id="id_indicator"]');
    const vAlMlField = document.querySelector('[id="id_v_al_ml"]');

    const VTitr = document.querySelector('[id="id_v_titr_ml"]')
    const ph = document.querySelector('[id="id_ph"]')

    const titrantValueField = document.getElementById('id_titrant_value_hidden');
    const tTitrField = document.getElementById('id_t_titr_hidden');

    // Функция для обновления видимости полей
    function updateVisibleFields(visibleFields) {
        // Очищаем значения всех полей перед обновлением видимости
        document.querySelectorAll('.measurement input[name]').forEach(input => {
            input.value = ''; // Очищаем значение поля
        });

        document.querySelectorAll('.measurement input[name]').forEach(input => {
            let fieldName = input.getAttribute('name');
            let label = input.previousElementSibling; // предполагается, что label идёт сразу перед input
            if (visibleFields.includes(fieldName)) {
                input.style.display = '';
                input.required = true; // делаем поле обязательным
                VTitr.required = false;
                ph.required = false;

                if (label && label.tagName.toLowerCase() === 'label') {
                    label.style.display = '';
                }
            } else {
                input.style.display = 'none';
                input.required = false
                if (label && label.tagName.toLowerCase() === 'label') {
                    label.style.display = 'none';
                }
            }
        });
    }

    // Функция для показа всех полей
    function showAllFields() {
        document.querySelectorAll('.measurement input[name]').forEach(input => {
            input.style.display = '';
            let label = input.previousElementSibling;
            if (label && label.tagName.toLowerCase() === 'label') {
                label.style.display = '';
            }
        });
    }

    function setFieldValue(field, value) {
        if (!field) {
            console.error('Поле не найдено:', field);
            return;
        }

        // Если поле является <select>
        if (field.tagName.toLowerCase() === 'select') {
            const option = Array.from(field.options).find(opt => opt.value === value || opt.text === value);
            if (option) {
                option.selected = true; // Выбираем соответствующий option
            } else {
                console.warn(`Значение "${value}" не найдено в выпадающем списке.`);
            }
        }
        // Если поле является <input> или <hidden>
        else if (['input', 'hidden'].includes(field.tagName.toLowerCase())) {
            field.value = value; // Устанавливаем значение напрямую
        } else {
            console.error('Неподдерживаемый тип элемента:', field.tagName);
        }
    }

    // Обработчик изменения точки отбора
    selectionPoint.addEventListener('change', function () {

        const selectedOptionText = this.options[this.selectedIndex].text;
        const probe = probes[selectedOptionText];

        if (probe) {
            // Устанавливаем значение для индикатора
            setFieldValue(indicatorField, probe.indicator);

             // Находим строку с нужным титрантом в таблице
            const titrantRow = Array.from(document.querySelectorAll('table tbody tr')).find(row => {
                return row.dataset.titrantName === probe.titrant;
            });

            if (titrantRow) {
                // Получаем данные из атрибутов data-*
                const titrantId = titrantRow.dataset.titrantId;
                const tTitr = titrantRow.dataset.tTitr;

                // Устанавливаем значения в скрытые поля
                titrantValueField.value = titrantId;
                tTitrField.value = tTitr;

                const titrantDisplay = document.getElementById('id_titrant_display');
                if (titrantDisplay) {
                    titrantDisplay.value = `${probe.titrant}, T титр: ${tTitr}`;
                }

                console.log(`Выбран титрант: ${probe.titrant}, T титр: ${tTitr}`);
            } else {
                const titrantDisplay = document.getElementById('id_titrant_display');
                console.error(`Титрант "${probe.titrant}" не найден в таблице.`);
                titrantDisplay.value = '';
            }


            // Обновляем видимость полей
            updateVisibleFields(probe.fields);

            // Устанавливаем значение для v_al_ml и скрываем/показываем поле
            if (probe.v_al_ml !== null) {
                vAlMlField.value = probe.v_al_ml; // Устанавливаем значение
                vAlMlField.style.display = ''; // Показываем поле
                vAlMlField.previousElementSibling.style.display = ''; // Показываем label
            } else {
                vAlMlField.value = ''; // Очищаем значение
                vAlMlField.style.display = 'none'; // Скрываем поле
                vAlMlField.previousElementSibling.style.display = 'none'; // Скрываем label
            }

        } else {
            // Если выбранная точка не найдена, возвращаем показ всех полей
            showAllFields();
        }
    });


    // Старый функционал с чекбоксами
    const repeatCheckboxCeh = document.getElementById('repeat_ceh');
    const repeatCheckboxLab = document.getElementById('repeat_lab');
    const idRepeatContainer = document.getElementById('id_repeat_container');
    const idRepeatChoiceField = document.getElementById('id_replaced_by');
    const replaceSourceInput = document.getElementById('id_replace_source');

    function toggleIdRepeat() {
        idRepeatContainer.style.display =
            (repeatCheckboxCeh.checked || repeatCheckboxLab.checked)
                ? 'block'
                : 'none';

        // Установка или удаление атрибута required
        if (repeatCheckboxCeh.checked || repeatCheckboxLab.checked) {
            idRepeatChoiceField.required = true;
        } else {
            idRepeatChoiceField.required = false;
            replaceSourceInput.value = '';
            clearRepeatFields(); // Очищаем поля, если повтор отменен
        }
    }
    // Обработчики для чекбоксов
    repeatCheckboxCeh.addEventListener('change', function () {
        if (this.checked) {
            repeatCheckboxLab.checked = false;
            replaceSourceInput.value = 'workshop';
        }
        toggleIdRepeat();
    });

    repeatCheckboxLab.addEventListener('change', function () {
        if (this.checked) {
            repeatCheckboxCeh.checked = false;
            replaceSourceInput.value = 'lab';
        }
        toggleIdRepeat();
    });



    // Новый функционал: автоматическое заполнение полей при выборе записи для повтора
    idRepeatChoiceField.addEventListener('change', function () {
        const recordId = this.value;

        if (recordId && (repeatCheckboxCeh.checked || repeatCheckboxLab.checked)) {
            fetch(`/lab/get-record-data/${recordId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data) {
                         document.querySelector('[id="id_fio"]').value = data.fio;

                        const selectionPointField = document.querySelector('[id="id_selection_point"]');
                        selectionPointField.value = data.selection_point;
                        selectionPointField.dispatchEvent(new Event("change"));  // <<< ВАЖНО: триггерим событие

                        document.querySelector('[id="id_us_def_time"]').value = data.user_defined_time;
                        console.log(data.user_defined_time)
                    }
                })
                .catch(error => console.error('Ошибка при получении данных:', error));
        } else {
            clearRepeatFields(); // Очищаем поля, если запись не выбрана
        }
    });

    // Функция для очистки полей, связанных с повтором
    function clearRepeatFields() {
        const fioField = document.querySelector('[id="id_fio"]');
        const selectionPointField = document.querySelector('[id="id_selection_point"]');
        const userTime = document.querySelector('[id="id_us_def_time"]');
        const replacedBy = document.querySelector('[id="id_replaced_by"]');

        if (fioField) fioField.value = '';
        if (selectionPointField) selectionPointField.value = '';
        if (userTime) userTime.value = '';
        if (replacedBy) replacedBy.value = ''; // очищаем выбор заменяемой записи
        replaceSourceInput.value = '';
    }

    // toggleIdRepeat уже есть — добавим безопасность при первом вызове
    function toggleIdRepeat() {
        idRepeatContainer.style.display =
            (repeatCheckboxCeh.checked || repeatCheckboxLab.checked)
                ? 'block'
                : 'none';

        if (repeatCheckboxCeh.checked || repeatCheckboxLab.checked) {
            idRepeatChoiceField.required = true;
        } else {
            idRepeatChoiceField.required = false;
            replaceSourceInput.value = '';
            idRepeatChoiceField.value = '';
            clearRepeatFields();
        }
    }

    // Обработчики для чекбоксов (без изменений)
    repeatCheckboxCeh.addEventListener('change', function () {
        if (this.checked) {
            repeatCheckboxLab.checked = false;
            replaceSourceInput.value = 'workshop';
        } else {
            replaceSourceInput.value = '';
        }
        toggleIdRepeat();
    });

    repeatCheckboxLab.addEventListener('change', function () {
        if (this.checked) {
            repeatCheckboxCeh.checked = false;
            replaceSourceInput.value = 'lab';
        } else {
            replaceSourceInput.value = '';
        }
        toggleIdRepeat();
    });

    // Автозаполнение при выборе записи для повтора
    idRepeatChoiceField.addEventListener('change', function () {
        const recordId = this.value;

        if (recordId && (repeatCheckboxCeh.checked || repeatCheckboxLab.checked)) {
            fetch(`/lab/get-record-data/${recordId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data && !data.error) {
                        const fioFieldEl = document.querySelector('[id="id_fio"]');
                        const selectionPointField = document.querySelector('[id="id_selection_point"]');
                        const userTime = document.querySelector('[id="id_us_def_time"]');

                        if (fioFieldEl) fioFieldEl.value = data.fio;
                        if (selectionPointField) {
                            selectionPointField.value = data.selection_point;
                            // триггерим change чтобы JS выставил titrant/v_al и т.д.
                            selectionPointField.dispatchEvent(new Event("change"));
                        }
                        if (userTime) userTime.value = data.user_defined_time;
                    } else {
                        clearRepeatFields();
                    }
                })
                .catch(error => {
                    console.error('Ошибка при получении данных:', error);
                    clearRepeatFields();
                });
        } else {
            clearRepeatFields(); // Очищаем поля, если запись не выбрана
        }
    });

});