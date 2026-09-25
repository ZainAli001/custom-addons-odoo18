/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart, useRef, useEffect } from "@odoo/owl";

const CHART_COLORS = {
    yellow: "#f0ad4e",
    grey: "#8c8c8c",
    green: "#28a745",
    red: "#dc3545",
    blue: "#3b82f6",
    purple: "#8b5cf6",
    pink: "#ec4899",
};

export class HeadcountDashboard extends Component {
    static template = "hr_headcount_dashboard.Dashboard";

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            filters: {
                region_id: false,
                zone_id: false,
                city: "",
                branch_id: false,
                division_id: false,
                department_id: false,
                sub_department_id: false,
                job_id: false,
                management_level_id: false,
                hr_grade_id: false,
                employment_type: false,
                employee_status: false,
                gender: false,
                date_from: this._defaultFrom(),
                date_to: this._defaultTo(),
            },
            options: {
                regions: [], zones: [], branches: [], divisions: [],
                departments: [], sub_departments: [], jobs: [],
                management_levels: [], hr_grades: [],
            },
            kpis: {},
            charts: {},
            employees: [],
            employeeCount: 0,
            page: 1,
            pageSize: 6,
            loading: true,
        });

        this.chartInstances = {};
        this.refs = {
            regionZone: useRef("chart_region_zone"),
            department: useRef("chart_department"),
            status: useRef("chart_status"),
            gender: useRef("chart_gender"),
            ftPt: useRef("chart_ft_pt"),
            trend: useRef("chart_trend"),
            joinersExits: useRef("chart_joiners_exits"),
            position: useRef("chart_position"),
        };

        onWillStart(async () => {
            this.state.options = await this.rpc("/hr_headcount_dashboard/filter_options", {});
            await this.loadData();
        });

        useEffect(
            () => {
                if (!this.state.loading) {
                    this.renderCharts();
                }
            },
            () => [this.state.charts]
        );
    }

    _defaultTo() {
        const d = new Date();
        return d.toISOString().slice(0, 10);
    }
    _defaultFrom() {
        const d = new Date();
        d.setMonth(d.getMonth() - 1);
        return d.toISOString().slice(0, 10);
    }

    async loadData() {
        this.state.loading = true;
        const result = await this.rpc("/hr_headcount_dashboard/data", {
            filters: this.state.filters,
            offset: (this.state.page - 1) * this.state.pageSize,
            limit: this.state.pageSize,
        });
        this.state.kpis = result.kpis;
        this.state.charts = result.charts;
        this.state.employees = result.employees;
        this.state.employeeCount = result.employee_count;
        this.state.loading = false;
    }

    onFilterChange(field, ev) {
        this.state.filters[field] = ev.target.value || false;
        this.state.page = 1;
        this.loadData();
    }

    onDateChange(field, ev) {
        this.state.filters[field] = ev.target.value;
        this.state.page = 1;
        this.loadData();
    }

    resetFilters() {
        for (const key of Object.keys(this.state.filters)) {
            if (key !== "date_from" && key !== "date_to") {
                this.state.filters[key] = key === "city" ? "" : false;
            }
        }
        this.state.page = 1;
        this.loadData();
    }

    prevPage() {
        if (this.state.page > 1) {
            this.state.page -= 1;
            this.loadData();
        }
    }
    nextPage() {
        if (this.state.page * this.state.pageSize < this.state.employeeCount) {
            this.state.page += 1;
            this.loadData();
        }
    }

    exportCsv() {
        const rows = [
            ["Employee Code", "Name", "Department", "Designation", "Branch", "Status"],
            ...this.state.employees.map((e) => [
                e.employee_code, e.name, e.department, e.designation, e.branch, e.status,
            ]),
        ];
        const csv = rows.map((r) => r.map((v) => `"${v || ""}"`).join(",")).join("\n");
        const blob = new Blob([csv], { type: "text/csv" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "employee_list.csv";
        link.click();
    }

    _destroyChart(key) {
        if (this.chartInstances[key]) {
            this.chartInstances[key].destroy();
            delete this.chartInstances[key];
        }
    }

    renderCharts() {
        const c = this.state.charts;
        if (!c || !window.Chart) {
            return;
        }

        // Headcount by Region / Zone (grouped bar)
        this._destroyChart("regionZone");
        if (this.refs.regionZone.el) {
            this.chartInstances.regionZone = new Chart(this.refs.regionZone.el, {
                type: "bar",
                data: {
                    labels: c.headcount_by_region_zone.labels,
                    datasets: [
                        { label: "Region", data: c.headcount_by_region_zone.region, backgroundColor: CHART_COLORS.yellow },
                        { label: "Zone", data: c.headcount_by_region_zone.zone, backgroundColor: CHART_COLORS.grey },
                    ],
                },
                options: { responsive: true, maintainAspectRatio: false },
            });
        }

        // Headcount by Department (horizontal bar)
        this._destroyChart("department");
        if (this.refs.department.el) {
            this.chartInstances.department = new Chart(this.refs.department.el, {
                type: "bar",
                data: {
                    labels: c.headcount_by_department.labels,
                    datasets: [{ data: c.headcount_by_department.values, backgroundColor: CHART_COLORS.yellow }],
                },
                options: {
                    indexAxis: "y", responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                },
            });
        }

        // Employee Status (donut)
        this._destroyChart("status");
        if (this.refs.status.el) {
            this.chartInstances.status = new Chart(this.refs.status.el, {
                type: "doughnut",
                data: {
                    labels: c.employee_status.labels,
                    datasets: [{
                        data: c.employee_status.values,
                        backgroundColor: [CHART_COLORS.green, CHART_COLORS.yellow, CHART_COLORS.blue, CHART_COLORS.purple, CHART_COLORS.red, CHART_COLORS.grey],
                    }],
                },
                options: { responsive: true, maintainAspectRatio: false, cutout: "70%" },
            });
        }

        // Gender Ratio (donut)
        this._destroyChart("gender");
        if (this.refs.gender.el) {
            this.chartInstances.gender = new Chart(this.refs.gender.el, {
                type: "doughnut",
                data: {
                    labels: c.gender_ratio.labels,
                    datasets: [{ data: c.gender_ratio.values, backgroundColor: [CHART_COLORS.blue, CHART_COLORS.pink, CHART_COLORS.grey] }],
                },
                options: { responsive: true, maintainAspectRatio: false, cutout: "65%" },
            });
        }

        // Full-time vs Part-time (donut)
        this._destroyChart("ftPt");
        if (this.refs.ftPt.el) {
            this.chartInstances.ftPt = new Chart(this.refs.ftPt.el, {
                type: "doughnut",
                data: {
                    labels: c.full_time_part_time.labels,
                    datasets: [{ data: c.full_time_part_time.values, backgroundColor: [CHART_COLORS.grey, CHART_COLORS.yellow] }],
                },
                options: { responsive: true, maintainAspectRatio: false, cutout: "70%" },
            });
        }

        // Monthly Headcount Trend (line)
        this._destroyChart("trend");
        if (this.refs.trend.el) {
            this.chartInstances.trend = new Chart(this.refs.trend.el, {
                type: "line",
                data: {
                    labels: c.monthly_headcount_trend.labels,
                    datasets: [
                        { label: "Total Headcount", data: c.monthly_headcount_trend.total_headcount, borderColor: CHART_COLORS.yellow, tension: 0.3 },
                        { label: "Active Headcount", data: c.monthly_headcount_trend.active_headcount, borderColor: CHART_COLORS.grey, tension: 0.3 },
                    ],
                },
                options: { responsive: true, maintainAspectRatio: false },
            });
        }

        // New Joiners vs Exits (grouped bar)
        this._destroyChart("joinersExits");
        if (this.refs.joinersExits.el) {
            this.chartInstances.joinersExits = new Chart(this.refs.joinersExits.el, {
                type: "bar",
                data: {
                    labels: c.new_joiners_vs_exits.labels,
                    datasets: [
                        { label: "New Joiners", data: c.new_joiners_vs_exits.new_joiners, backgroundColor: CHART_COLORS.green },
                        { label: "Exits", data: c.new_joiners_vs_exits.exits, backgroundColor: CHART_COLORS.red },
                    ],
                },
                options: { responsive: true, maintainAspectRatio: false },
            });
        }

        // Position Status (donut)
        this._destroyChart("position");
        if (this.refs.position.el) {
            const p = c.position_status;
            this.chartInstances.position = new Chart(this.refs.position.el, {
                type: "doughnut",
                data: {
                    labels: ["Filled", "Vacant", "Open"],
                    datasets: [{ data: [p.filled, p.vacant, p.open], backgroundColor: [CHART_COLORS.green, CHART_COLORS.yellow, CHART_COLORS.blue] }],
                },
                options: { responsive: true, maintainAspectRatio: false, cutout: "70%" },
            });
        }
    }
}

registry.category("actions").add("hr_headcount_dashboard", HeadcountDashboard);
