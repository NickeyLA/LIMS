const labConfigurations = {
    "ХA": {
        "indicators": ["V2O5", "Fe дисп", "H2SO4", "CaO", "SO4"],
        "key": "1"
    },
    "Физико-механический анализ": {
        "indicators": ["Плотность", "Влажность"],
        "key": "1"
    },
    "Общий анализ": {
        "indicators": ["pH", "Температура"],
        "key": "1"
    }
};

let loadedIndicators = [];
let currentTemplate = null;
let selectedLabKey = null;

document.addEventListener('DOMContentLoaded', function () {
    const fioDataTitr = document.getElementById('fio-data-titr');
    const lastFioTitr = fioDataTitr?.dataset.lastFioTitr;
    const fioFieldTitr = document.querySelector('[id="id_fio_titr"]');

    if (lastFioTitr && fioFieldTitr) {
        fioFieldTitr.value = lastFioTitr;
    }

    const probeSelect = document.getElementById('id_probe');
    const indicatorSelect = document.getElementById('id_probe_indicator');
    const comment = document.getElementById('id_comment');
    const name_probe = document.getElementById('id_name_probe');
    const comment_for_lab = document.getElementById('id_comment_for_lab');
    const skeyInput = document.getElementById('skey');
    const saveBtn = document.getElementById('save-analysis-button');
    const analysisForm = document.getElementById('analysis-form');
    const analyzedIndicatorsDropdown = document.getElementById('analyzed-indicators-dropdown');
    const deleteIndicatorBtn = document.getElementById('delete-indicator-btn');

    if (skeyInput) skeyInput.disabled = true;
    if (saveBtn) saveBtn.disabled = true;
    if (deleteIndicatorBtn) deleteIndicatorBtn.disabled = true;

    // Функция для обновления таблицы результатов
    function updateAnalysisTable(probeId) {
        fetch(`/lab_xa/get_probe_data/${probeId}/`)
            .then(response => response.json())
            .then(data => {
                const analysisTableBody = document.querySelector('#analysis-results-table tbody');
                analysisTableBody.innerHTML = '';

                data.analysis_results.forEach(result => {
                    const row = document.createElement('tr');
                    const fioCell = document.createElement('td');
                    fioCell.textContent = result.fio;

                    const selectionPointCell = document.createElement('td');
                    selectionPointCell.textContent = result.selection_point_name;

                    const nameProbeCell = document.createElement('td');
                    nameProbeCell.textContent = result.name_probe;

                    const indicatorCell = document.createElement('td');
                    indicatorCell.textContent = result.indicator_name;

                    const valuesCell = document.createElement('td');
                    valuesCell.innerHTML = result.values
                        .map(v => `${v.name} - ${v.value}`)
                        .join('<br>');

                    const timeCell = document.createElement('td');
                    timeCell.textContent = result.user_defined_time;

                    row.appendChild(fioCell);
                    row.appendChild(selectionPointCell);
                    row.appendChild(nameProbeCell);
                    row.appendChild(indicatorCell);
                    row.appendChild(valuesCell);
                    row.appendChild(timeCell);

                    analysisTableBody.insertBefore(row, analysisTableBody.firstChild);
                });
            })
            .catch(error => {
                console.error('Ошибка при обновлении таблицы:', error);
            });
    }

    // Обновленная функция для выпадающего списка с показателями для удаления
    function updateAnalyzedIndicatorsDropdown(analysisResults) {
        const dropdown = document.getElementById('analyzed-indicators-dropdown');
        dropdown.innerHTML = '<option value="">Выберите показатель для удаления</option>';

        const seen = new Map();
        analysisResults.forEach(result => {
            if (!seen.has(result.probe_indicator_id)) {
                seen.set(result.probe_indicator_id, result.indicator_name);
            }
        });
        seen.forEach((name, id) => {
            const option = document.createElement('option');
            option.value = id;
            option.textContent = name;
            dropdown.appendChild(option);
        });
        dropdown.disabled = seen.size === 0;
        if (deleteIndicatorBtn) deleteIndicatorBtn.disabled = true;
    }

    probeSelect?.addEventListener('change', function() {
        const probeId = this.value;
        console.log('Выбранный шифр:', probeId);

        indicatorSelect.innerHTML = '<option value="">Загрузка...</option>';
        const selectionPointInput = document.getElementById('id_selection_point');
        const user_defined_time = document.getElementById('id_analys_user_defined_time');

        if (skeyInput) {
            skeyInput.value = '';
            skeyInput.disabled = true;
        }
        if (saveBtn) saveBtn.disabled = true;
        selectedLabKey = null;

        fetch(`/lab_xa/get_probe_data/${probeId}/`)
            .then(response => response.json())
            .then(data => {
                loadedIndicators = data.indicators;

                indicatorSelect.innerHTML = '<option value="">Выберите показатель</option>';
                data.indicators.forEach(indicator => {
                    const option = document.createElement('option');
                    option.value = indicator.id;
                    option.textContent = indicator.name;
                    indicatorSelect.appendChild(option);
                });

                if (selectionPointInput && data.selection_point) {
                    selectionPointInput.value = data.selection_point;
                } else if (selectionPointInput) {
                    selectionPointInput.value = '';
                }

                if (user_defined_time && data.probe_datetime) {
                    user_defined_time.value = data.probe_datetime;
                } else if (user_defined_time) {
                    user_defined_time.value = '';
                }

                if (comment) {
                    comment.value = data.comment || '';
                }
                if (comment_for_lab) {
                    comment_for_lab.value = data.comment_for_lab || '';
                }
                if (name_probe) {
                    name_probe.value = data.name_probe || '';
                }

                updateAnalysisTable(probeId);
                updateAnalyzedIndicatorsDropdown(data.analysis_results);

            })
            .catch(error => {
                console.error('Ошибка при получении данных по пробе:', error);
                indicatorSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
                if (selectionPointInput) {
                    selectionPointInput.value = '';
                }
            });
    });

    indicatorSelect?.addEventListener('change', function () {
        const selectedId = this.value;
        const selectedOption = this.options[this.selectedIndex];
        const selectedIndicatorName = selectedOption.textContent;

        const indicator = loadedIndicators.find(i => i.id == selectedId);
        const template = indicator?.template || null;

        const container = document.getElementById('analysis-template-fields');
        container.innerHTML = ''; // Очищаем динамические поля
        currentTemplate = null;
        selectedLabKey = null;

        if (skeyInput) {
            skeyInput.value = '';
            skeyInput.disabled = true;
        }
        if (saveBtn) saveBtn.disabled = true;

        for (const labName in labConfigurations) {
            if (labConfigurations[labName].indicators.includes(selectedIndicatorName)) {
                selectedLabKey = labConfigurations[labName].key;
                if (selectedLabKey === null) {
                    if (skeyInput) skeyInput.disabled = true;
                    if (saveBtn) saveBtn.disabled = false;
                } else {
                    if (skeyInput) skeyInput.disabled = false;
                    if (saveBtn) saveBtn.disabled = true;
                }
                break;
            }
        }

        if (selectedLabKey === null && selectedId !== "") {
            if (skeyInput) skeyInput.disabled = true;
            if (saveBtn) saveBtn.disabled = false;
        } else if (selectedId === "") {
            if (skeyInput) skeyInput.disabled = true;
            if (saveBtn) saveBtn.disabled = true;
        }

        const RSA_ELEMENTS = [
            'V2O5 (РСА)', 'Fe общ', 'CaO общ', 'CaO ввод', 'TiO2', 'Mn', 'MnO',
            'Al2O3', 'SiO2', 'MgO', 'Cr2O3'
        ];

        const AES_ISP_ELEMENTS = [
            'V2O5 (АЭС ИСП)', 'Fe', 'As', 'K', 'Ca', 'Al', 'Ni', 'Pb', 'P', 'Si', 'Cu',
            'SO4', 'Ti', 'Mg', 'Zr', 'V', 'Cr', 'Mo', 'Zn', 'Mn', 'W', 'Na'
        ];

        const selectedIndicatorNameLower = selectedIndicatorName.toLowerCase();
        let elementsToUse = [];

        if (selectedIndicatorNameLower.includes('рса')) {
            elementsToUse = RSA_ELEMENTS;
        } else if (selectedIndicatorNameLower.includes('аэс исп')) {
            elementsToUse = AES_ISP_ELEMENTS;
        }

        const rawComment = comment?.value.toLowerCase() || '';
        const commentParts = rawComment.split(',').map(item => item.trim()).filter(Boolean);
        const filteredElements = elementsToUse.filter(elem => commentParts.includes(elem.toLowerCase()));
        elementsToUse = filteredElements;

        container.innerHTML = '';

        if (elementsToUse.length > 0) {
            currentTemplate = null;
            const rowDiv = document.createElement('div');
            rowDiv.classList.add('row');

            elementsToUse.forEach((name, index) => {
                const columnDiv = document.createElement('div');
                columnDiv.classList.add('column');

                const label = document.createElement('label');
                label.textContent = name;

                const hiddenNameInput = document.createElement('input');
                hiddenNameInput.type = 'hidden';
                hiddenNameInput.name = 'name_value';
                hiddenNameInput.value = name;

                const input = document.createElement('input');
                input.type = 'text';
                input.name = `value | ${name}`;
                input.classList.add('custom-input');

                columnDiv.appendChild(label);
                columnDiv.appendChild(hiddenNameInput);
                columnDiv.appendChild(input);
                rowDiv.appendChild(columnDiv);
            });

            container.appendChild(rowDiv);
        } else if (template) {
            currentTemplate = template;
            const rowDiv = document.createElement('div');
            rowDiv.classList.add('row');

            template.fields.forEach((field, index) => {
                const columnDiv = document.createElement('div');
                columnDiv.classList.add('column');

                const label = document.createElement('label');
                label.textContent = field.name;

                const hiddenNameInput = document.createElement('input');
                hiddenNameInput.type = 'hidden';
                hiddenNameInput.name = 'name_value';
                hiddenNameInput.value = field.name;

                const input = document.createElement('input');
                input.type = 'text';
                input.name = `value | ${field.name}`;
                input.value = field.value || '';
                input.classList.add('custom-input');

                if (!field.editable) {
                    input.setAttribute('readonly', true);
                    input.style.backgroundColor = '#eee';
                }

                columnDiv.appendChild(label);
                columnDiv.appendChild(hiddenNameInput);
                columnDiv.appendChild(input);
                rowDiv.appendChild(columnDiv);
            });

            container.appendChild(rowDiv);

        } else if (!template && elementsToUse.length === 0 && selectedIndicatorName) {
            // Если нет шаблона, не RSA/АЭС ИСП — создаём поле по умолчанию
            const rowDiv = document.createElement('div');
            rowDiv.classList.add('row');

            const columnDiv = document.createElement('div');
            columnDiv.classList.add('column');

            const label = document.createElement('label');
            label.textContent = selectedIndicatorName;

            const hiddenNameInput = document.createElement('input');
            hiddenNameInput.type = 'hidden';
            hiddenNameInput.name = 'name_value';
            hiddenNameInput.value = selectedIndicatorName;

            const input = document.createElement('input');
            input.type = 'text';
            input.name = `value | ${selectedIndicatorName}`;
            input.classList.add('custom-input');

            columnDiv.appendChild(label);
            columnDiv.appendChild(hiddenNameInput);
            columnDiv.appendChild(input);
            rowDiv.appendChild(columnDiv);

            container.appendChild(rowDiv);
        }

    });

    skeyInput?.addEventListener('input', function() {
        if (selectedLabKey !== null && this.value === selectedLabKey) {
            if (saveBtn) saveBtn.disabled = false;
        } else if (selectedLabKey === null) {
            if (saveBtn) saveBtn.disabled = false;
        } else {
            if (saveBtn) saveBtn.disabled = true;
        }
    });

    // Добавляем обработчик для выпадающего списка показателей для удаления
    analyzedIndicatorsDropdown?.addEventListener('change', function() {
        if (deleteIndicatorBtn) {
            deleteIndicatorBtn.disabled = !this.value;
        }
    });

    // Добавляем обработчик для кнопки удаления
    deleteIndicatorBtn?.addEventListener('click', async function() {
        const probeIndicatorId = analyzedIndicatorsDropdown.value;
        if (!probeIndicatorId) {
            alert('Пожалуйста, выберите показатель для удаления.');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('probe_indicator_id', probeIndicatorId);
            const response = await fetch(analysisForm.dataset.deleteUrl, {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
            });
            const data = await response.json();
            if (response.ok && data.status === 'ok') {
                location.reload();
            } else {
                throw new Error(data.error || 'Неизвестная ошибка сервера.');
            }
        } catch (error) {
            console.error('Ошибка при удалении:', error);
            alert(`Не удалось удалить записи: ${error.message}`);
        }
    });

    const titrantCheckboxes = [
        document.querySelector('input[name="v_titr_1_checkbox"]'),
        document.querySelector('input[name="v_titr_2_checkbox"]'),
        document.querySelector('input[name="v_titr_3_checkbox"]'),
        document.querySelector('input[name="v_titr_4_checkbox"]')
    ];

    const titrantInputs = [
        document.querySelector('input[name="v_titr_1"]'),
        document.querySelector('input[name="v_titr_2"]'),
        document.querySelector('input[name="v_titr_3"]'),
        document.querySelector('input[name="v_titr_4"]')
    ];

    const submitButton = document.querySelector('button[type="submit"]');
    const usedValuesInput = document.querySelector('input[name="used_values"]');

    function updateFormState() {
        let values = [];
        let usedValues = '';

        titrantCheckboxes.forEach((checkbox, index) => {
            const input = titrantInputs[index];
            if (checkbox?.checked) {
                input?.setAttribute('required', true);
                values.push(parseFloat(input.value) || 0);
                usedValues += (index + 1).toString();
            } else {
                input?.removeAttribute('required');
            }
        });

        if (usedValuesInput) {
            usedValuesInput.value = usedValues;
        }

        let maxDelta = 0;
        if (values.length >= 2) {
            for (let i = 0; i < values.length; i++) {
                for (let j = i + 1; j < values.length; j++) {
                    let delta = Math.abs(values[i] - values[j]);
                    if (delta > maxDelta) {
                        maxDelta = delta;
                    }
                }
            }
        } else {
            maxDelta = 0;
        }

        if (submitButton) {
            if (maxDelta > 0.20) {
                submitButton.disabled = true;
                submitButton.style.backgroundColor = 'grey';
            } else {
                submitButton.disabled = false;
                submitButton.style.backgroundColor = '';
            }
        }
    }

    titrantCheckboxes.forEach(cb => cb?.addEventListener('change', updateFormState));
    titrantInputs.forEach(input => input?.addEventListener('input', updateFormState));
    updateFormState();

    const initData = document.getElementById('analysis-init-data');
    const lastFio = initData?.dataset.lastFio;
    const lastProbe = initData?.dataset.lastProbe;

    const fioField = document.getElementById('id_fio');
    const probeField = document.getElementById('id_probe');

    if (lastFio && fioField) {
        fioField.value = lastFio;
    }

    if (lastProbe && probeField) {
        probeField.value = lastProbe;
        probeField.dispatchEvent(new Event("change", { bubbles: true }));
    }

    saveBtn?.addEventListener('click', function () {
        if (!analysisForm.checkValidity()) {
            analysisForm.reportValidity();
            return;
        }

        if (selectedLabKey !== null && skeyInput.value !== selectedLabKey) {
            alert('Неверный ключ для выбранного показателя!');
            return;
        }

        const formData = new FormData(analysisForm);
        formData.delete('name_value');
        formData.delete('value');

        const fieldInputs = document.querySelectorAll('#analysis-template-fields input[name^="value |"]');
        const fieldNames = document.querySelectorAll('#analysis-template-fields input[name="name_value"]');

        if (fieldInputs.length !== fieldNames.length) {
            alert('Ошибка: количество имен и значений не совпадает!');
            return;
        }

        fieldNames.forEach((nameInput, index) => {
            const valueInput = fieldInputs[index];
            if (nameInput.value && valueInput.value) {
                formData.append('name_value', nameInput.value);
                formData.append('value', valueInput.value);
            }
        });

        const selectedIndicatorText = indicatorSelect.options[indicatorSelect.selectedIndex]?.textContent || '';
        formData.append('selected_indicator', selectedIndicatorText);

        console.log('Отправляемые данные формы:');
        const formDataObject = {};
        for (let pair of formData.entries()) {
            formDataObject[pair[0]] = pair[1];
        }
        console.table(formDataObject);

        fetch('/lab_xa/save_analysis/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(async response => {
            console.log("Статус ответа:", response.status);

            let text = await response.text();
            console.log("Тело ответа:", text);

            if (response.ok) {
                location.reload();
            } else {
                alert('Ошибка при сохранении: ' + text);
            }
        })
        .catch(error => {
            console.error('Ошибка при сохранении:', error);
            alert('Произошла ошибка');
        });
    });
});