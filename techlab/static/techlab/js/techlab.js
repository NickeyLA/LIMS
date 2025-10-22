document.addEventListener("DOMContentLoaded", () => {
    // ===== 1. Кнопка "Очистить всё" =====
    const clearBtn = document.getElementById("clear-all-btn");
    if (clearBtn) {
        clearBtn.addEventListener("click", () => {
            document.querySelectorAll("input[type=checkbox]").forEach(cb => cb.checked = false);
        });
    }

    // ===== 2. Выпадающий список "Шаблоны" =====
    const templateSelect = document.getElementById("template-select");
    if (templateSelect) {
        templateSelect.addEventListener("change", (e) => {
            // Сначала очистим все чекбоксы
            document.querySelectorAll("input[type=checkbox]").forEach(cb => cb.checked = false);

            switch (e.target.value) {
                case "thermohydrolysis":
                    toggleIndicators([
                        {point: 17, indicators: ["ph_density"]},
                        {point: 18, indicators: ["ph_density", "v2o5"]},
                        {point: 19, indicators: ["ph_density", "v2o5"]},
                        {point: 36, indicators: ["ph_density"]},
                    ]);
                    break;

                case "mgso4":
                    toggleIndicators([
                        {point: 9, indicators: ["v2o5"]},
                        {point: 11, indicators: ["v2o5"]},
                        {point: 3, indicators: ["mgso4"]},
                    ]);
                    break;

                case "p-p":
                    toggleIndicators([
                        {point: 9, indicators: ["v2o5"]},
                        {point: 11, indicators: ["v2o5"]},
                    ]);
                    break;

                case "acid":
                    toggleIndicators([
                        {point: 9, indicators: ["ph_density", "v2o5"]},
                        {point: 11, indicators: ["ph_density", "v2o5"]},
                        {point: 16, indicators: ["ph_density", "h2so4"]},
                        {point: 10, indicators: ["ph_density", "v2o5"]},
                        {point: 12, indicators: ["ph_density", "v2o5", "susp"]},
                    ]);
                    break;

                case "reactor5":
                    toggleIndicators([
                        {point: 6, indicators: ["ph_density", "v2o5"]},
                    ]);
                    break;
            }
        });
    }

    function toggleIndicators(config) {
        config.forEach(item => {
            item.indicators.forEach(ind => {
                const selector = `input[name="indicators_point_${item.point}"][value="${ind}"]`;
                const checkbox = document.querySelector(selector);
                if (checkbox) checkbox.checked = true;
            });
        });
    }

    // ===== 3. Сбор данных и скачивание =====
    const form = document.querySelector("form");

    if (form && !form.dataset.listenerAdded) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const dateFrom = document.getElementById("id_date_from").value;
            const dateTo = document.getElementById("id_date_to").value;
            const reportType = document.getElementById("select-type").value;

            const data = {
                date_from: dateFrom,
                date_to: dateTo,
                report_type: reportType,
                points: []
            };

            document.querySelectorAll("input[type=checkbox]:checked").forEach(cb => {
                const pointId = cb.name.replace("indicators_point_", "");
                let point = data.points.find(p => p.point_id === pointId);
                if (!point) {
                    point = {point_id: pointId, indicators: []};
                    data.points.push(point);
                }
                point.indicators.push(cb.value);
            });

            console.log("Сформированные данные:", data);

            fetch("/techlab/download-excel/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
                body: JSON.stringify(data),
            })
            .then(response => {
                if (!response.ok) throw new Error("Ошибка при формировании отчёта");
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "Выгрузка.xlsx";
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                alert("Не удалось скачать файл: " + error);
            });
        });

        // пометка, что обработчик уже навешан
        form.dataset.listenerAdded = "true";
    }
});
