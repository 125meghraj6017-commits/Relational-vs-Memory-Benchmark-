
"use strict";

const $ = (selector) => document.querySelector(selector);

let performanceChart = null;
let latestResults = [];
let chartScale = "linear";
let toastTimer = null;

const numberFormat = new Intl.NumberFormat("en-US");

function showToast(message) {
    const toast = $("#toast");
    toast.textContent = message;
    toast.classList.add("show");

    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        toast.classList.remove("show");
    }, 3500);
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

function formatTime(value) {
    return Number(value).toFixed(3);
}

function updateMetrics(results) {
    const avlAverage = results.reduce(
        (sum, row) => sum + row.avl_time,
        0
    ) / results.length;

    const sqliteAverage = results.reduce(
        (sum, row) => sum + row.sqlite_time,
        0
    ) / results.length;

    $("#metric-datasets").textContent =
        String(results.length).padStart(2, "0");

    $("#metric-avl").innerHTML =
        `${formatTime(avlAverage)} <small>µs</small>`;

    $("#metric-sqlite").innerHTML =
        `${formatTime(sqliteAverage)} <small>µs</small>`;

    const allCorrect = results.every(
        (row) => row.correctness
    );

    $("#metric-status").textContent =
        allCorrect ? "PASS" : "CHECK";

    $("#metric-status").style.color =
        allCorrect ? "#54d6ad" : "#ff9999";

    $("#validation-detail").textContent =
        allCorrect ? "All tested configurations" : "Review results";
}

function renderTableBody(rows, target, full = false) {
    if (!rows.length) {
        target.innerHTML = `
            <tr>
                <td colspan="${full ? 6 : 4}" class="empty-table">
                    No benchmark results available.
                </td>
            </tr>`;
        return;
    }

    target.innerHTML = rows.map((row) => {
        const statusClass = row.correctness ? "pass" : "fail";
        const statusText = row.correctness ? "PASS" : "CHECK";

        if (full) {
            return `
                <tr>
                    <td class="row-number">${numberFormat.format(row.dataset_size)}</td>
                    <td class="time-avl">${formatTime(row.avl_time)}</td>
                    <td class="time-sql">${formatTime(row.sqlite_time)}</td>
                    <td>${row.avl_found ? "Yes" : "No"}</td>
                    <td>${row.sqlite_found ? "Yes" : "No"}</td>
                    <td><span class="result-badge ${statusClass}">${statusText}</span></td>
                </tr>`;
        }

        return `
            <tr>
                <td class="row-number">${numberFormat.format(row.dataset_size)}</td>
                <td class="time-avl">${formatTime(row.avl_time)} µs</td>
                <td class="time-sql">${formatTime(row.sqlite_time)} µs</td>
                <td><span class="result-badge ${statusClass}">${statusText}</span></td>
            </tr>`;
    }).join("");
}

function renderChart(results) {
    const canvas = $("#performance-chart");
    const emptyState = $("#chart-empty");

    if (performanceChart) {
        performanceChart.destroy();
        performanceChart = null;
    }

    if (!results.length) {
        emptyState.style.display = "flex";
        return;
    }

    emptyState.style.display = "none";

    const styles = getComputedStyle(document.body);
    const muted = styles.getPropertyValue("--muted").trim() || "#828ca5";
    const border = styles.getPropertyValue("--border").trim() || "#252d40";

    performanceChart = new Chart(canvas, {
        type: "line",
        data: {
            labels: results.map(
                (row) => numberFormat.format(row.dataset_size)
            ),
            datasets: [
                {
                    label: "AVL Tree",
                    data: results.map((row) => row.avl_time),
                    borderColor: "#a294ff",
                    backgroundColor: "rgba(162, 148, 255, 0.12)",
                    pointBackgroundColor: "#a294ff",
                    pointBorderColor: "#17142a",
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 7,
                    borderWidth: 2.5,
                    tension: 0.32,
                    fill: true
                },
                {
                    label: "SQLite",
                    data: results.map((row) => row.sqlite_time),
                    borderColor: "#70a7ff",
                    backgroundColor: "rgba(112, 167, 255, 0.05)",
                    pointBackgroundColor: "#70a7ff",
                    pointBorderColor: "#172238",
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 7,
                    borderWidth: 2.5,
                    tension: 0.32,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: "index",
                intersect: false
            },
            animation: {
                duration: 850,
                easing: "easeOutQuart"
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: "#171d2d",
                    borderColor: "#343d57",
                    borderWidth: 1,
                    padding: 12,
                    titleColor: "#edf1ff",
                    bodyColor: "#b6c1d8",
                    displayColors: true,
                    callbacks: {
                        label(context) {
                            return `${context.dataset.label}: ${
                                Number(context.raw).toFixed(3)
                            } µs`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "NUMBER OF RECORDS",
                        color: muted,
                        font: { size: 10, weight: "bold" }
                    },
                    ticks: { color: muted, font: { size: 10 } },
                    grid: { color: border + "55" },
                    border: { display: false }
                },
                y: {
                    type: chartScale,
                    beginAtZero: chartScale === "linear",
                    title: {
                        display: true,
                        text: "AVERAGE SEARCH TIME (µs)",
                        color: muted,
                        font: { size: 10, weight: "bold" }
                    },
                    ticks: {
                        color: muted,
                        font: { size: 10 },
                        callback(value) {
                            return Number(value).toLocaleString("en-US");
                        }
                    },
                    grid: { color: border + "75" },
                    border: { display: false }
                }
            }
        }
    });
}

function renderResults(results) {
    latestResults = results;

    updateMetrics(results);

    renderTableBody(
        results.slice(0, 5),
        $("#preview-table")
    );

    renderTableBody(
        results,
        $("#full-table"),
        true
    );

    renderChart(results);

    $("#chart-caption").textContent =
        `${results.length} dataset configurations`;

    $("#metric-status").title =
        "Validation reflects the returned search results. " +
        "The current Python engine checks the final search result.";

    $("#export-csv").disabled = results.length === 0;
}

function showPage(page) {
    const titles = {
        overview: "Overview",
        performance: "Performance",
        results: "Results explorer",
        methodology: "Methodology"
    };

    document.querySelectorAll(".nav-item").forEach((button) => {
        button.classList.toggle(
            "active",
            button.dataset.page === page
        );
    });

    $("#breadcrumb-page").textContent = titles[page] || "Overview";

    $("#overview-chart").classList.toggle(
        "hidden",
        page !== "overview" && page !== "performance"
    );

    document.querySelector(".lower-grid").classList.toggle(
        "hidden",
        page !== "overview"
    );

    $("#results-page").classList.toggle(
        "hidden",
        page !== "results"
    );

    $("#methodology-page").classList.toggle(
        "hidden",
        page !== "methodology"
    );

    if (page === "performance") {
        $("#overview-chart").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    } else {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
}

async function runBenchmark() {
    const button = $("#run-benchmark");

    button.disabled = true;
    button.innerHTML = "<span>◌</span> Running benchmark...";

    showToast("Benchmark started. Please wait.");

    try {
        const response = await fetch("/api/benchmark", {
            method: "POST",
            headers: { "Accept": "application/json" }
        });

        const payload = await response.json();

        if (!response.ok || !payload.success) {
            throw new Error(
                payload.error || "The benchmark could not complete."
            );
        }

        renderResults(payload.results);

        showPage("overview");

        showToast("Benchmark completed successfully.");
    } catch (error) {
        showToast(error.message || "Unable to run benchmark.");

        console.error("Benchmark error:", error);
    } finally {
        button.disabled = false;
        button.innerHTML =
            '<span>▶</span> Run benchmark <span class="button-arrow">↗</span>';
    }
}

function exportCSV() {
    if (!latestResults.length) {
        showToast("Run a benchmark before exporting results.");
        return;
    }

    const columns = [
        "Dataset Size",
        "AVL Search Time (microseconds)",
        "SQLite Search Time (microseconds)",
        "AVL Found",
        "SQLite Found",
        "Correctness"
    ];

    const rows = latestResults.map((row) => [
        row.dataset_size,
        row.avl_time,
        row.sqlite_time,
        row.avl_found,
        row.sqlite_found,
        row.correctness
    ]);

    const csv = [columns, ...rows]
        .map((row) =>
            row.map((value) => {
                const text = String(value);
                return `"${text.replace(/"/g, '""')}"`;
            }).join(",")
        )
        .join("\r\n");

    const blob = new Blob(
        ["\uFEFF", csv],
        { type: "text/csv;charset=utf-8;" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "benchmark_results.csv";
    link.click();

    URL.revokeObjectURL(url);

    showToast("CSV export downloaded.");
}

document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
        showPage(button.dataset.page);
    });
});

$("#run-benchmark").addEventListener("click", runBenchmark);

$("#view-results").addEventListener("click", () => {
    showPage("results");
});

$("#all-results").addEventListener("click", () => {
    showPage("results");
});

$("#export-csv").addEventListener("click", exportCSV);

document.querySelectorAll(".chart-tab").forEach((button) => {
    button.addEventListener("click", () => {
        chartScale = button.dataset.scale;

        document.querySelectorAll(".chart-tab").forEach((tab) => {
            tab.classList.toggle("active", tab === button);
        });

        renderChart(latestResults);
    });
});

$("#theme-toggle").addEventListener("click", () => {
    document.body.classList.toggle("light-theme");

    if (latestResults.length) {
        renderChart(latestResults);
    }

    showToast(
        document.body.classList.contains("light-theme")
            ? "Light appearance enabled."
            : "Dark appearance enabled."
    );
});

$("#metric-datasets").textContent = "05";

renderChart([]);
