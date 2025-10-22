    document.addEventListener('DOMContentLoaded', function() {
        // Правила видимости индикаторов
        const indicatorRules = {
            'ОТК': {
                'Алюминий (в.к.)': ['Mn', 'Cu', 'Si', 'Fe', 'Mg', 'Zn', 'Ti', 'C', '№ места', 'поставщик', 'основной элемент'],
                'Известняк (в.к.)': ['CaO общ', 'Al2O3', 'Fe', 'MgO', 'MnO', 'P', 'SiO2', 'TiO2', 'машина/вагон', 'фракция', 'поставщик', 'грансостав', 'пылевидные и глинистые включения', 'глина в комках'],
                'Кислота серная (в.к.)': ['H2SO4', 'органолептика', '№ вагона', 'цвет', 'органика', 'запах', 'мех. примеси'],
                'Шлак НТМК (в.к.)': ['№ вагона', 'CaO общ', 'TiO2', 'V2O5', 'Cr2O3', 'MnO', 'Fe', 'М/в', 'определение марки'],
                'FeV I период': ['№ плавки', 'V', 'C'],
                'FeV III период': ['№ плавки', 'C', 'S', 'V', 'Mn', 'Si', 'Cu', 'Al', 'P', 'Cr', 'Ti'],
                'FeV конечный металл': ['№ плавки', 'V', 'C', 'Mn', 'Si', 'Cu', 'Al', 'P', 'S', 'Cr', 'Ti'],
                'FeV80 (паспорт)': ['№ плавки', 'вес', 'кол-во мест', 'V', 'C', 'Mn', 'Si', 'Cu', 'Al', 'As', 'P', 'S', 'Cr', 'Ni', 'Ti', 'Mo'],
                'FeV80 фр 2-10 СГП': ['№ плавки', 'вес', 'кол-во мест', 'V', 'C', 'Mn', 'Si', 'Cu', 'Al', 'As', 'P', 'S', 'Cr', 'Ni'],
                'V2O5 (паспорт)': ['№ партии', 'кол-во биг-бегов', 'вес', 'V2O5', 'SiO2', 'TiO2', 'Mn', 'P', 'S', 'CaO', 'Fe'],
                'V2O5 короба': ['№ короба', 'вес', 'CaO', 'TiO2', 'V2O5', 'Cr2O3', 'Mn', 'Fe', 'S', 'определение марки'],
                'Шлам отвальный': ['V2O5', 'V2O5 k/r'],
                'Зашлакованность металлоотсева': ['примечание', 'процент', 'V2O5', 'C', 'CaCO3', 'влага'],
                'Зашлакованность (1,2,3)': ['грансостав'],
                'Известь ГМЦ (в.к.)': ['CaO акт', 'поставщик'],
                'Конвейер 18а': ['V2O5', 'влага'],
                'Шихта на обжиг': ['Fe дисп', 'влага', 'CaO общ', 'Fe общ', 'TiO2', 'V2O5', 'Cr2O3', 'MnO', 'М (общ.)', 'Fe общ', 'М (ввод.)'],
                'Шихта обожженная': ['V2O5', 'V2O5 k/r', 'V2O5 pH', 'Тех. вскр.', 'pH вскр.', 'грансостав', 'Fe дисп'],
                'Известь ЭМЦ (в.к.)': ['CaO акт', 'C', 'P', 'CaO+MgO', 'примечание'],
                'шлак 80 раф': ['№ плавки', 'V2O5', 'CaO', 'Al2O3', 'MgO', 'SiO2', 'MnO', 'Fe', 'TiO2', 'ZnO', 'Fe общ'],
                'Шлак 80 сливной период 1': ['№ плавки', 'V2O5', 'CaO', 'Al2O3', 'MgO', 'SiO2', 'MnO', 'Fe', 'TiO2', 'ZnO', 'Fe общ'],
                'Шлак 80 сливной период 3': ['№ плавки', 'V2O5', 'CaO', 'Al2O3', 'MgO', 'SiO2', 'MnO', 'Fe', 'TiO2', 'ZnO', 'Fe общ'],
                'КЖС': ['Fe2O3', 'CaO общ', 'MnO'],
                'Щебень макадам': ['Al2O3', 'MgO', 'SiO2', 'CaO общ', 'V2O5', 'MnO', 'FeO', 'TiO2', 'ZnO', 'Fe'],
            },
            'ТЛ': {
                'Кек 5 реактора': ['V2O5 (РСА)'],
                '5 реактор ТЛ': ['V2O5'],
                'Магнитная часть из короба': ['V2O5 (РСА)', 'Fe дисп'],
                'Питание магнитного сепаратора': ['V2O5 (РСА)', 'Fe дисп'],
                'Немагнитная часть после сеп.': ['V2O5 (РСА)', 'Fe дисп'],
                'Вода УМП НАЛКО': ['V2O5 (АЭС ИСП)', 'Ca', 'Mn', 'Al', 'Si', 'Fe', 'Na', 'SO4'],
                'Вода озерная НАЛКО': ['V2O5 (АЭС ИСП)', 'Ca', 'Mn', 'Al', 'Si', 'Fe', 'Na', 'SO4'],
                'Вода 3 выпуска': ['V2O5 (АЭС ИСП)', 'Ca', 'Mn', 'Al', 'Si', 'Fe', 'Na', 'SO4'],
                'Верхний слив сгустителя №2': ['V2O5 (АЭС ИСП)', 'Ca', 'Mn', 'Al', 'Si', 'Fe', 'Na', 'SO4'],
                'Вода с г/о ПП': ['V2O5 (РСА)'],
                'Сливной шлак': ['V2O5 (РСА)', 'CaO общ'],
            },
            'СОП': {
                'СОП 78-2021': ['V2O5', 'V2O5 k/r', 'V2O5 pH', 'Тех. вскр.', 'pH вскр.', 'грансостав', 'Fe дисп'],// Шихта обожженная
                'СОП 75-2021': ['V2O5', 'V2O5 k/r', 'V2O5 pH', 'Тех. вскр.', 'pH вскр.', 'грансостав', 'Fe дисп'],
                'СОП 6-2017Д': ['V2O5', 'V2O5 k/r'],// Шлам отвальный
                'СОП 07-2022': ['V2O5', 'V2O5 k/r'],// Шлам отвальный
                'СОП 67-2022': ['V2O5', 'V2O5 k/r'],// Шлам отвальный
                'СОП 08-2022': ['V2O5', 'V2O5 k/r'],// Шлам отвальный
                'СОП 82-2021': ['V2O5', 'V2O5 k/r'],// Шлам отвальный
                'СОП 93-2025': ['Fe дисп', 'влага', 'CaO общ', 'Fe общ', 'TiO2', 'V2O5', 'Cr2O3', 'MnO', 'М (общ.)', 'Fe общ', 'М (ввод.)'],// Шихта на обжиг
                '81-2018Д': ['CaO общ', 'Al2O3', 'Fe', 'MgO', 'MnO', 'P', 'SiO2', 'TiO2', 'машина/вагон', 'фракция', 'поставщик', 'грансостав', 'пылевидные и глинистые включения', 'глина в комках'],// Известняк (в.к.)
                'КО 25-2024': ['H2SO4', 'органолептика', '№ вагона', 'цвет', 'органика', 'запах', 'мех. примеси'],'Кислота серная (в.к.)': ['H2SO4', 'органолептика', '№ вагона', 'цвет', 'органика', 'запах', 'мех. примеси'],//Кислота серная (в.к.)
            }
        };



        // Получаем элементы формы
        const clientSelect = document.querySelector('select[name="client"]');
        const selectionPointSelect = document.querySelector('select[name="selection_point"]');
        const commentField = document.getElementById('id_comment');
        const buttonsContainer = document.querySelector('.buttons');
        const probesDropdown = document.getElementById('probes-dropdown');
        const deleteProbesBtn = document.getElementById('delete-probes-btn');

        // Создаем контейнер для кнопок слева
        const leftButtonsContainer = document.createElement('div');
        leftButtonsContainer.className = 'left-buttons';
        leftButtonsContainer.style.display = 'flex';
        leftButtonsContainer.style.gap = '10px';
        leftButtonsContainer.style.marginRight = 'auto';

        // Удаляем старые кнопки, если они уже есть
        document.querySelectorAll('.custom-action-btn').forEach(btn => btn.remove());

        // Создаем кнопку "Показать все"
        const showAllBtn = document.createElement('button');
        showAllBtn.type = 'button';
        showAllBtn.textContent = 'Показать все показатели';
        showAllBtn.classList.add('btn', 'btn', 'custom-action-btn');

        // Создаем кнопку "Очистить всё"
        const clearAllBtn = document.createElement('button');
        clearAllBtn.type = 'button';
        clearAllBtn.textContent = 'Очистить всё';
        clearAllBtn.classList.add('btn', 'btn', 'custom-action-btn');

        // Добавляем кнопки в левый контейнер
        leftButtonsContainer.appendChild(showAllBtn);
        leftButtonsContainer.appendChild(clearAllBtn);

        // Вставляем левый контейнер в основной контейнер кнопок
        buttonsContainer.prepend(leftButtonsContainer);

        // --- Общие функции ---

        // Функция для сброса всех чекбоксов
        function clearAllCheckboxes() {
            document.querySelectorAll('.indicator-item input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            updateRsaCheckboxState();
            updateAesIspCheckboxState();
        }


        // Функция обновления комментария
        function updateComment(checkbox) {
            const label = checkbox.closest('.indicator-item').querySelector('label').textContent.trim();
            let currentComment = commentField.value;

            const words = currentComment.split(', ').map(s => s.trim()).filter(Boolean);

            if (checkbox.checked) {
                if (!words.includes(label)) {
                    words.push(label);
                }
            } else {
                const index = words.indexOf(label);
                if (index !== -1) {
                    words.splice(index, 1);
                }
            }

            commentField.value = words.join(', ');
        }

        // --- Логика для РСА ---
        let rsaMainCheckbox = null;
        let rsaMainCheckboxItem = null;
        const rsaGroupHeader = Array.from(document.querySelectorAll('.indicator-group h3')).find(h3 => h3.textContent.trim() === 'РСА');
        let rsaGroup = null;

        if (rsaGroupHeader) {
            rsaGroup = rsaGroupHeader.closest('.indicator-group');
            if (rsaGroup) {
                Array.from(rsaGroup.querySelectorAll('.indicator-item')).forEach(item => {
                    const labelElement = item.querySelector('label');
                    if (labelElement && labelElement.textContent.trim() === 'РСА') {
                        rsaMainCheckboxItem = item;
                        rsaMainCheckbox = item.querySelector('input[type="checkbox"]');
                    }
                });
            }
        }

        // Скрываем и делаем неуправляемым главный чекбокс "РСА"
        if (rsaMainCheckboxItem) {
            rsaMainCheckboxItem.style.display = 'none';
            rsaMainCheckboxItem.style.pointerEvents = 'none';
            const rsaLabel = rsaMainCheckboxItem.querySelector('label');
            if (rsaLabel) {
                rsaLabel.style.pointerEvents = 'none';
            }
        }

        // Функция для управления состоянием главного чекбокса "РСА"
        function updateRsaCheckboxState() {
            if (!rsaMainCheckbox || !rsaGroup) {
                return;
            }

            const rsaSubCheckboxes = Array.from(rsaGroup.querySelectorAll('.indicator-item input[type="checkbox"]'))
                .filter(cb => {
                    const labelElement = cb.closest('.indicator-item').querySelector('label');
                    return labelElement && labelElement.textContent.trim() !== 'РСА';
                });

            const anyRsaSubCheckboxChecked = rsaSubCheckboxes.some(cb => cb.checked);
            rsaMainCheckbox.checked = anyRsaSubCheckboxChecked;
        }

        // --- Логика для АЭС ИСП ---
        let aesIspMainCheckbox = null;
        let aesIspMainCheckboxItem = null;
        const aesIspGroupHeader = Array.from(document.querySelectorAll('.indicator-group h3')).find(h3 => h3.textContent.trim() === 'АЭС ИСП');
        let aesIspGroup = null;

        if (aesIspGroupHeader) {
            aesIspGroup = aesIspGroupHeader.closest('.indicator-group');
            if (aesIspGroup) {
                Array.from(aesIspGroup.querySelectorAll('.indicator-item')).forEach(item => {
                    const labelElement = item.querySelector('label');
                    if (labelElement && labelElement.textContent.trim() === 'АЭС ИСП') {
                        aesIspMainCheckboxItem = item;
                        aesIspMainCheckbox = item.querySelector('input[type="checkbox"]');
                    }
                });
            }
        }

        // Скрываем и делаем неуправляемым главный чекбокс "АЭС ИСП"
        if (aesIspMainCheckboxItem) {
            aesIspMainCheckboxItem.style.display = 'none';
            aesIspMainCheckboxItem.style.pointerEvents = 'none';
            const aesIspLabel = aesIspMainCheckboxItem.querySelector('label');
            if (aesIspLabel) {
                aesIspLabel.style.pointerEvents = 'none';
            }
        }

        // Функция для управления состоянием главного чекбокса "АЭС ИСП"
        function updateAesIspCheckboxState() {
            if (!aesIspMainCheckbox || !aesIspGroup) {
                return;
            }

            const aesIspSubCheckboxes = Array.from(aesIspGroup.querySelectorAll('.indicator-item input[type="checkbox"]'))
                .filter(cb => {
                    const labelElement = cb.closest('.indicator-item').querySelector('label');
                    return labelElement && labelElement.textContent.trim() !== 'АЭС ИСП';
                });

            const anyAesIspSubCheckboxChecked = aesIspSubCheckboxes.some(cb => cb.checked);
            aesIspMainCheckbox.checked = anyAesIspSubCheckboxChecked;
        }

        // --- Обновленная функция видимости индикаторов ---
        function updateIndicatorVisibility(initialLoad = false) {
            const client = clientSelect.options[clientSelect.selectedIndex].text;
            const selectionPoint = selectionPointSelect.options[selectionPointSelect.selectedIndex].text;

            if (client === 'ИЦ') {
                document.querySelectorAll('.indicator-item').forEach(item => {
                    if (rsaMainCheckboxItem && item === rsaMainCheckboxItem ||
                        aesIspMainCheckboxItem && item === aesIspMainCheckboxItem) {
                        return;
                    }
                    item.style.display = 'flex';
                    const checkbox = item.querySelector('input[type="checkbox"]');
                    checkbox.disabled = false;
                    if (initialLoad) checkbox.checked = false;
                    item.classList.remove('disabled-indicator');
                });
                updateRsaCheckboxState();
                updateAesIspCheckboxState();
                return;
            }

            const allowedIndicators = indicatorRules[client]?.[selectionPoint];

            document.querySelectorAll('.indicator-item').forEach(item => {
                if (rsaMainCheckboxItem && item === rsaMainCheckboxItem ||
                    aesIspMainCheckboxItem && item === aesIspMainCheckboxItem) {
                    return;
                }

                const checkbox = item.querySelector('input[type="checkbox"]');
                const label = item.querySelector('label').textContent.trim();

                if (!allowedIndicators || allowedIndicators.includes(label)) {
                    item.style.display = 'flex';
                    checkbox.disabled = false;
                    if (!initialLoad) checkbox.checked = true;
                    item.classList.remove('disabled-indicator');
                } else {
                    item.style.display = 'none';
                    checkbox.checked = false;
                }
            });
            updateRsaCheckboxState();
            updateAesIspCheckboxState();
        }

        function showAllIndicators() {
            document.querySelectorAll('.indicator-item').forEach(item => {
                if (rsaMainCheckboxItem && item === rsaMainCheckboxItem ||
                    aesIspMainCheckboxItem && item === aesIspMainCheckboxItem) {
                    return;
                }
                item.style.display = 'flex';
                const checkbox = item.querySelector('input[type="checkbox"]');
                checkbox.disabled = false;
                item.classList.remove('disabled-indicator');
            });
            updateRsaCheckboxState();
            updateAesIspCheckboxState();
        }

        // --- Назначение обработчиков событий ---
        clientSelect.addEventListener('change', () => updateIndicatorVisibility());
        selectionPointSelect.addEventListener('change', () => updateIndicatorVisibility());
        showAllBtn.addEventListener('click', showAllIndicators);
        clearAllBtn.addEventListener('click', clearAllCheckboxes);

        // Инициализация при загрузке
        updateIndicatorVisibility(true);

        // Назначаем обработчики всем чекбоксам из группы РСА (кроме главного "РСА")
        if (rsaGroup) {
            const allRsaCheckboxesInGroup = Array.from(rsaGroup.querySelectorAll('.indicator-item input[type="checkbox"]'));
            allRsaCheckboxesInGroup.forEach((checkbox) => {
                const labelElement = checkbox.closest('.indicator-item').querySelector('label');
                if (labelElement && labelElement.textContent.trim() !== 'РСА') {
                    checkbox.addEventListener('change', () => {
                        updateComment(checkbox);
                        updateRsaCheckboxState();
                    });
                }
            });
        }

        // Назначаем обработчики всем чекбоксам из группы АЭС ИСП (кроме главного "АЭС ИСП")
        if (aesIspGroup) {
            const allAesIspCheckboxesInGroup = Array.from(aesIspGroup.querySelectorAll('.indicator-item input[type="checkbox"]'));
            allAesIspCheckboxesInGroup.forEach((checkbox) => {
                const labelElement = checkbox.closest('.indicator-item').querySelector('label');
                if (labelElement && labelElement.textContent.trim() !== 'АЭС ИСП') {
                    checkbox.addEventListener('change', () => {
                        updateComment(checkbox);
                        updateAesIspCheckboxState();
                    });
                }
            });
        }

        // Удаляем функцию updateAnalyzedIndicatorsDropdown, так как она не соответствует текущей логике
        // Вместо этого список проб уже заполнен в шаблоне через prob_list

        // Активация/деактивация кнопки удаления
        probesDropdown.addEventListener('change', function() {
            deleteProbesBtn.disabled = !this.value; // Активируем кнопку, если выбрана проба
        });

        // Обработчик нажатия на кнопку удаления
        deleteProbesBtn.addEventListener('click', async function() {
            const probeId = probesDropdown.value;
            if (!probeId) {
                alert('Пожалуйста, выберите пробу для удаления.');
                return;
            }

            try {
                const formData = new FormData();
                formData.append('probe_id', probeId);
                const response = await fetch('/lab_otk/delete_probe/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });
                const data = await response.json();
                if (response.ok && data.status === 'ok') {
                    location.reload(); // Перезагружаем страницу для обновления таблицы
                } else {
                    throw new Error(data.error || 'Неизвестная ошибка сервера.');
                }
            } catch (error) {
                console.error('Ошибка при удалении:', error);
                alert(`Не удалось удалить пробу: ${error.message}`);
            }
        });
        // Функция для сброса всех чекбоксов и очистки комментария
        function clearAllCheckboxes() {
            document.querySelectorAll('.indicator-item input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            commentField.value = ''; // Очищаем поле комментария
            updateRsaCheckboxState();
            updateAesIspCheckboxState();
        }

        // Новая вспомогательная функция для проверки, принадлежит ли чекбокс группам РСА или АЭС ИСП
        function isRsaOrAesIspCheckbox(checkbox) {
            const parentGroup = checkbox.closest('.indicator-group');
            if (!parentGroup) return false;
            const groupHeader = parentGroup.querySelector('h3');
            if (!groupHeader) return false;
            const groupName = groupHeader.textContent.trim();
            return groupName === 'РСА' || groupName === 'АЭС ИСП';
        }

        // Обновленная функция видимости индикаторов
        function updateIndicatorVisibility(initialLoad = false) {
            const client = clientSelect.options[clientSelect.selectedIndex].text;
            const selectionPoint = selectionPointSelect.options[selectionPointSelect.selectedIndex].text;

            if (client === 'ИЦ') {
                document.querySelectorAll('.indicator-item').forEach(item => {
                    if (rsaMainCheckboxItem && item === rsaMainCheckboxItem ||
                        aesIspMainCheckboxItem && item === aesIspMainCheckboxItem) {
                        return;
                    }
                    item.style.display = 'flex';
                    const checkbox = item.querySelector('input[type="checkbox"]');
                    checkbox.disabled = false;
                    if (initialLoad) {
                        checkbox.checked = false;
                        // Очищаем комментарий для чекбоксов РСА и АЭС ИСП
                        if (isRsaOrAesIspCheckbox(checkbox)) {
                            updateComment(checkbox);
                        }
                    }
                    item.classList.remove('disabled-indicator');
                });
                updateRsaCheckboxState();
                updateAesIspCheckboxState();
            }

            const allowedIndicators = indicatorRules[client]?.[selectionPoint];

            document.querySelectorAll('.indicator-item').forEach(item => {
                if (rsaMainCheckboxItem && item === rsaMainCheckboxItem ||
                    aesIspMainCheckboxItem && item === aesIspMainCheckboxItem) {
                    return;
                }

                const checkbox = item.querySelector('input[type="checkbox"]');
                const label = item.querySelector('label').textContent.trim();

                if (!allowedIndicators || allowedIndicators.includes(label)) {
                    item.style.display = 'flex';
                    checkbox.disabled = false;
                    if (!initialLoad) {
                        checkbox.checked = true;
                        // Обновляем комментарий только для РСА и АЭС ИСП
                        if (isRsaOrAesIspCheckbox(checkbox)) {
                            updateComment(checkbox);
                        }
                    }
                    item.classList.remove('disabled-indicator');
                } else {
                    item.style.display = 'none';
                    checkbox.checked = false;
                    // Обновляем комментарий только для РСА и АЭС ИСП
                    if (isRsaOrAesIspCheckbox(checkbox)) {
                        updateComment(checkbox);
                    }
                }
            });
            updateRsaCheckboxState();
            updateAesIspCheckboxState();
    }

        // Инициализация состояний главных чекбоксов при загрузке страницы
        updateRsaCheckboxState();
        updateAesIspCheckboxState();

        // Автоматическое заполнение поля "Наименование пробы" при смене точки отбора
        const nameProbeField = document.getElementById('id_name_probe');

        if (selectionPointSelect && nameProbeField) {
            selectionPointSelect.addEventListener('change', () => {
                const selectedText = selectionPointSelect.options[selectionPointSelect.selectedIndex].text;
                nameProbeField.value = selectedText;
            });

            // Заполняем сразу при загрузке (если уже что-то выбрано)
            if (selectionPointSelect.selectedIndex > -1) {
                nameProbeField.value = selectionPointSelect.options[selectionPointSelect.selectedIndex].text;
            }
        }

    });

    /*
                'Кислота серная (в.к.)': ['H2SO4', 'органолептика'],
                'Известь (в.к.)': ['CaO акт'],
                'Известь ЭМЦ (в.к.)': ['CaO акт', 'MgO', 'CaO', 'C', 'грансостав'],
                'Алюминий (в.к.)': ['АЭС ИСП', 'C'],
                'Шлак НТМК (в.к.)': ['CaO', 'TiO2', 'V2O5', 'Cr2O3', 'MnO', 'Fe', 'М/в'],
                'Известняк (в.к.)': ['АЭС ИСП'],
                'Зашлакованность': ['V2O5', 'C', 'шлак', 'влага'],
                'Шихта на обжиг': ['Fe дисп', 'влажность', 'грансостав', 'АЭС ИСП', 'C'],
                'Шихта обожженная': ['V2O5', 'V2O5 k/r', 'V2O5 pH', 'грансостав'],
                'Шлам отвальный': ['V2O5', 'V2O5 k/r'],
                'Металлопродукт': ['влажность'],
                'Конвейер 18а': ['V2O5', 'влажность'],
                'V2O5 (паспорт)': ['V2O5', 'S', 'РСА', 'АЭС ИСП'],
                'V2O5 короба': ['S', 'РСА'],
                'FeV II период': ['C'],
                'FeV III период': ['C', 'S'],
                'FeV конечный металл': ['C', 'S', 'АЭС ИСП'],
                'FeV80 (паспорт)': ['V', 'C', 'S', 'АЭС ИСП'],
                'FeV80 фр 2-10 СГП': ['V', 'C', 'S', 'АЭС ИСП'],
    */