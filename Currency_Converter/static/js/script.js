(function () {
    "use strict";

    const API = {
        convert:    "/api/convert",
        history:    "/api/history",
        favorites:  "/api/favorites",
        trend:      "/api/trend",
    };

    const $ = (sel) => document.querySelector(sel);

    const els = {
        html:            document.documentElement,
        themeToggle:     $("#themeToggle"),
        converterForm:   $("#converterForm"),
        amount:          $("#amount"),
        amountSymbol:    $("#amountSymbol"),
        fromCurrency:    $("#fromCurrency"),
        toCurrency:      $("#toCurrency"),
        swapBtn:         $("#swapBtn"),
        convertBtn:      $("#convertBtn"),
        favoriteBtn:     $("#favoriteBtn"),
        clearBtn:        $("#clearBtn"),
        resultBox:       $("#resultBox"),
        resultFlag:      $("#resultFlag"),
        resultValue:     $("#resultValue"),
        rateText:        $("#rateText"),
        copyBtn:         $("#copyBtn"),
        updatedTime:     $("#updatedTime"),
        alertArea:       $("#alertArea"),
        spinnerOverlay:  $("#spinnerOverlay"),
        favoritesList:   $("#favoritesList"),
        trendCanvas:     $("#trendChart"),
        historyBody:     $("#historyBody"),
        historyCount:    $("#historyCount"),
        clearHistoryBtn: $("#clearHistoryBtn"),
        year:            $("#year"),
    };

    let trendChart = null;
    let lastResult = null;
    const TREND_FROM = "USD";
    const TREND_TO = "INR";

    function showSpinner(show) {
        els.spinnerOverlay.classList.toggle("d-none", !show);
        els.convertBtn.disabled = show;
        if (show) {
            els.convertBtn.innerHTML =
                '<span class="spinner-border spinner-border-sm me-2"></span>Converting...';
        } else {
            els.convertBtn.innerHTML =
                '<i class="bi bi-calculator me-1"></i> Convert';
        }
    }

    function showAlert(message, type) {
        type = type || "info";
        const icon = {
            success: "bi-check-circle-fill",
            danger:  "bi-exclamation-triangle-fill",
            warning: "bi-exclamation-triangle-fill",
            info:    "bi-info-circle-fill",
        }[type] || "bi-info-circle-fill";

        const div = document.createElement("div");
        div.className = `alert alert-${type} d-flex align-items-center gap-2`;
        div.setAttribute("role", "alert");
        div.innerHTML =
            `<i class="bi ${icon}"></i><div>${escapeHtml(message)}</div>`;
        els.alertArea.appendChild(div);
        setTimeout(() => {
            div.style.transition = "opacity .4s ease";
            div.style.opacity = "0";
            setTimeout(() => div.remove(), 400);
        }, 4500);
    }

    function clearAlerts() {
        els.alertArea.innerHTML = "";
    }

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    function fmt(n) {
        const num = Number(n);
        if (!isFinite(num)) return "0.00";
        return num.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 4,
        });
    }

    function fmtTime(value) {
        if (!value) return "—";
        let d;
        if (typeof value === "number") {
            d = new Date(value * 1000);
        } else {
            d = new Date(value);
        }
        if (isNaN(d.getTime())) return String(value);
        return d.toLocaleString(undefined, {
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    }

    function flagClass(code) {
        return `fi fi-${String(code || "").toLowerCase()}`;
    }

    const Theme = {
        init() {
            const saved = localStorage.getItem("cc-theme");
            const prefersDark = window.matchMedia &&
                window.matchMedia("(prefers-color-scheme: dark)").matches;
            this.apply(saved || (prefersDark ? "dark" : "light"));

            els.themeToggle.addEventListener("click", () => {
                const next = els.html.getAttribute("data-bs-theme") === "dark"
                    ? "light" : "dark";
                this.apply(next);
            });
        },
        apply(mode) {
            els.html.setAttribute("data-bs-theme", mode);
            localStorage.setItem("cc-theme", mode);
            const icon = els.themeToggle.querySelector("i");
            if (icon) {
                icon.className = mode === "dark"
                    ? "bi bi-sun-fill" : "bi bi-moon-stars-fill";
            }
            if (trendChart) renderTrend(trendChart._lastData);
        },
    };

    const Converter = {
        init() {
            this.updateAmountSymbol();
            els.fromCurrency.addEventListener("change", () => this.updateAmountSymbol());
            els.swapBtn.addEventListener("click", () => this.swap());
            els.converterForm.addEventListener("submit", (e) => {
                e.preventDefault();
                this.convert();
            });
            els.clearBtn.addEventListener("click", () => this.clearForm());
            els.copyBtn.addEventListener("click", () => this.copyResult());
            els.favoriteBtn.addEventListener("click", () => Favorites.toggleCurrent());
        },

        updateAmountSymbol() {
            const opt = els.fromCurrency.options[els.fromCurrency.selectedIndex];
            const sym = opt ? opt.getAttribute("data-symbol") : "$";
            els.amountSymbol.textContent = sym || "$";
        },

        swap() {
            const f = els.fromCurrency.value;
            els.fromCurrency.value = els.toCurrency.value;
            els.toCurrency.value = f;
            this.updateAmountSymbol();
            if (!els.resultBox.classList.contains("d-none")) this.convert();
        },

        async convert() {
            clearAlerts();
            const amount = els.amount.value.trim();
            const from = els.fromCurrency.value;
            const to = els.toCurrency.value;

            if (!amount || isNaN(amount) || Number(amount) < 0) {
                els.amount.classList.add("is-invalid");
                showAlert("Please enter a valid amount.", "warning");
                return;
            }
            els.amount.classList.remove("is-invalid");

            const url = `${API.convert}?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}&amount=${encodeURIComponent(amount)}`;
            showSpinner(true);
            try {
                const res = await fetch(url);
                const json = await res.json();
                if (!res.ok || !json.success) {
                    throw new Error(json.error || "Conversion failed.");
                }
                this.renderResult(json.data);
                lastResult = json.data;
                History.load();
                Trend.load();
            } catch (err) {
                this.hideResult();
                showAlert(err.message || "Something went wrong.", "danger");
            } finally {
                showSpinner(false);
            }
        },

        renderResult(data) {
            const toOpt = els.toCurrency.options[els.toCurrency.selectedIndex];
            const flag = toOpt ? toOpt.getAttribute("data-flag") : "";
            const sym = toOpt ? toOpt.getAttribute("data-symbol") : "";

            els.resultFlag.className = flagClass(flag);
            els.resultValue.textContent = fmt(data.result);

            const rateTxt = `1 ${data.from} = ${fmt(data.rate)} ${data.to}`;
            els.rateText.textContent = rateTxt;
            els.updatedTime.textContent = "Updated " + fmtTime(data.updated);

            els.resultBox.classList.remove("d-none");
            els.resultBox.style.animation = "none";
            void els.resultBox.offsetWidth;
            els.resultBox.style.animation = "";
        },

        hideResult() {
            els.resultBox.classList.add("d-none");
            lastResult = null;
        },

        clearForm() {
            els.amount.value = "";
            els.amount.classList.remove("is-invalid");
            this.hideResult();
            clearAlerts();
            els.amount.focus();
        },

        async copyResult() {
            if (!lastResult) return;
            const text = `${fmt(lastResult.amount)} ${lastResult.from} = ${fmt(lastResult.result)} ${lastResult.to}`;
            try {
                await navigator.clipboard.writeText(text);
                const icon = els.copyBtn.querySelector("i");
                const original = icon ? icon.className : "";
                if (icon) icon.className = "bi bi-check-lg";
                showAlert("Result copied to clipboard.", "success");
                setTimeout(() => { if (icon) icon.className = original; }, 1500);
            } catch {
                showAlert("Could not copy to clipboard.", "warning");
            }
        },
    };

    const Favorites = {
        init() {
            this.load();
        },

        async load() {
            try {
                const res = await fetch(API.favorites);
                const json = await res.json();
                if (json.success) this.render(json.data || []);
            } catch {
            }
        },

        render(items) {
            if (!items.length) {
                els.favoritesList.innerHTML =
                    '<span class="text-secondary small">No favorites yet. Tap the star to add a pair.</span>';
                return;
            }
            els.favoritesList.innerHTML = "";
            items.forEach((fav) => {
                const chip = document.createElement("span");
                chip.className = "fav-chip";
                chip.title = `${fav.from_curr} → ${fav.to_curr} (click to use)`;
                chip.innerHTML =
                    `<span class="${flagClass(favFromFlag(fav.from_curr))}"></span>` +
                    `<span>${escapeHtml(fav.from_curr)}</span>` +
                    `<i class="bi bi-arrow-right-short"></i>` +
                    `<span class="${flagClass(favToFlag(fav.to_curr))}"></span>` +
                    `<span>${escapeHtml(fav.to_curr)}</span>` +
                    `<i class="bi bi-x-lg fav-remove" title="Remove"></i>`;
                chip.addEventListener("click", (e) => {
                    if (e.target.classList.contains("fav-remove")) return;
                    els.fromCurrency.value = fav.from_curr;
                    els.toCurrency.value = fav.to_curr;
                    Converter.updateAmountSymbol();
                    Converter.convert();
                });
                chip.querySelector(".fav-remove").addEventListener("click", (e) => {
                    e.stopPropagation();
                    this.remove(fav.from_curr, fav.to_curr);
                });
                els.favoritesList.appendChild(chip);
            });
        },

        async toggleCurrent() {
            const from = els.fromCurrency.value;
            const to = els.toCurrency.value;
            const existing = els.favoritesList.querySelector(".fav-chip");
            const already = Array.from(els.favoritesList.querySelectorAll(".fav-chip"))
                .some((c) => c.textContent.includes(from) && c.textContent.includes(to));

            if (already) {
                await this.remove(from, to);
                showAlert(`Removed ${from} → ${to} from favorites.`, "info");
                return;
            }
            try {
                const res = await fetch(API.favorites, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ from, to }),
                });
                const json = await res.json();
                if (json.success) {
                    showAlert(`Saved ${from} → ${to} as a favorite.`, "success");
                    this.load();
                } else {
                    showAlert(json.error || "Could not save favorite.", "warning");
                }
            } catch {
                showAlert("Could not save favorite.", "danger");
            }
        },

        async remove(from, to) {
            try {
                const url = `${API.favorites}?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`;
                const res = await fetch(url, { method: "DELETE" });
                const json = await res.json();
                if (json.success) this.load();
            } catch {
                showAlert("Could not remove favorite.", "danger");
            }
        },
    };

    function favFromFlag(code) {
        const opt = findOption(els.fromCurrency, code);
        return opt ? opt.getAttribute("data-flag") : code.slice(0, 2).toLowerCase();
    }
    function favToFlag(code) {
        const opt = findOption(els.toCurrency, code);
        return opt ? opt.getAttribute("data-flag") : code.slice(0, 2).toLowerCase();
    }
    function findOption(select, code) {
        return Array.from(select.options).find((o) => o.value === code);
    }

    const History = {
        init() {
            this.load();
            els.clearHistoryBtn.addEventListener("click", () => this.clear());
        },

        async load() {
            try {
                const res = await fetch(API.history);
                const json = await res.json();
                if (json.success) this.render(json.data || []);
            } catch {
            }
        },

        render(rows) {
            els.historyCount.textContent = rows.length;
            if (!rows.length) {
                els.historyBody.innerHTML =
                    '<tr><td colspan="7" class="text-center text-secondary py-4">No conversions yet.</td></tr>';
                return;
            }
            els.historyBody.innerHTML = rows.map((r, i) => {
                const fromFlag = flagFor(r.from_curr);
                const toFlag = flagFor(r.to_curr);
                return `
                <tr>
                    <td class="text-secondary">${i + 1}</td>
                    <td><span class="curr-code"><span class="fi ${fromFlag}"></span>${escapeHtml(r.from_curr)}</span></td>
                    <td><span class="curr-code"><span class="fi ${toFlag}"></span>${escapeHtml(r.to_curr)}</span></td>
                    <td class="text-end">${fmt(r.amount)}</td>
                    <td class="text-end fw-semibold">${fmt(r.result)}</td>
                    <td class="text-end">${fmt(r.rate)}</td>
                    <td class="text-end text-secondary small">${escapeHtml(fmtTime(r.created_at))}</td>
                </tr>`;
            }).join("");
        },

        async clear() {
            try {
                const res = await fetch(API.history, { method: "DELETE" });
                const json = await res.json();
                if (json.success) {
                    this.render([]);
                    showAlert("History cleared.", "success");
                }
            } catch {
                showAlert("Could not clear history.", "danger");
            }
        },
    };

    function flagFor(code) {
        const from = findOption(els.fromCurrency, code);
        const to = findOption(els.toCurrency, code);
        const opt = from || to;
        if (opt) return `fi-${opt.getAttribute("data-flag")}`;
        return `fi-${String(code).slice(0, 2).toLowerCase()}`;
    }

    const Trend = {
        init() {
            if (typeof Chart === "undefined") return;
            this.load();
        },

        async load() {
            try {
                const url = `${API.trend}?from=${encodeURIComponent(TREND_FROM)}&to=${encodeURIComponent(TREND_TO)}`;
                const res = await fetch(url);
                const json = await res.json();
                if (json.success) renderTrend(json.data);
            } catch {
            }
        },
    };

    function renderTrend(data) {
        if (typeof Chart === "undefined" || !els.trendCanvas || !data) return;
        const series = (data.series || [])
            .filter((p) => Number.isFinite(Number(p.rate)));
        if (!series.length) return;
        const labels = series.map((p) => p.label);
        const rates = series.map((p) => Number(p.rate));
        const minRate = Math.min(...rates);
        const maxRate = Math.max(...rates);
        const range = maxRate - minRate;
        const padding = range > 0 ? range * 0.25 : Math.abs(maxRate || 1) * 0.01;

        const isDark = els.html.getAttribute("data-bs-theme") === "dark";
        const grid = isDark ? "rgba(255,255,255,0.08)" : "rgba(20,30,70,0.07)";
        const tick = isDark ? "#9aa3b8" : "#6b7280";
        const primary = getComputedStyle(document.documentElement)
            .getPropertyValue("--app-primary").trim() || "#4f46e5";

        const cfg = {
            type: "line",
            data: {
                labels,
                datasets: [{
                    label: `${data.from}/${data.to}`,
                    data: rates,
                    borderColor: primary,
                    backgroundColor: hexToRgba(primary, 0.15),
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3,
                    pointBackgroundColor: primary,
                    pointBorderColor: isDark ? "#161a26" : "#ffffff",
                    pointHoverRadius: 6,
                    spanGaps: false,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                normalized: true,
                interaction: {
                    intersect: false,
                    mode: "index",
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => `1 ${data.from} = ${fmt(ctx.parsed.y)} ${data.to}`,
                        },
                    },
                },
                scales: {
                    x: {
                        type: "category",
                        offset: false,
                        ticks: { color: tick },
                        grid: { color: grid },
                    },
                    y: {
                        type: "linear",
                        reverse: false,
                        min: Math.max(0, minRate - padding),
                        max: maxRate + padding,
                        ticks: {
                            color: tick,
                            callback: (value) => fmt(value),
                        },
                        grid: { color: grid },
                    },
                },
            },
        };

        if (trendChart) {
            trendChart.data = cfg.data;
            trendChart.options = cfg.options;
            trendChart._lastData = data;
            trendChart.update();
        } else {
            trendChart = new Chart(els.trendCanvas, cfg);
            trendChart._lastData = data;
        }
    }

    function hexToRgba(hex, alpha) {
        hex = (hex || "").replace("#", "");
        if (hex.length === 3) {
            hex = hex.split("").map((c) => c + c).join("");
        }
        const r = parseInt(hex.slice(0, 2), 16) || 79;
        const g = parseInt(hex.slice(2, 4), 16) || 70;
        const b = parseInt(hex.slice(4, 6), 16) || 229;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    document.addEventListener("DOMContentLoaded", () => {
        if (els.year) els.year.textContent = new Date().getFullYear();
        Theme.init();
        Converter.init();
        Favorites.init();
        History.init();
        Trend.init();
    });
})();
