/** @odoo-module **/

import {
    Component,
    useState,
    onMounted,
    onWillStart,
    onWillUnmount,
    useRef,
} from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadBundle } from "@web/core/assets";


export class ListViewAction extends Component {

    static template = "employee_dashboard.ListView";


    setup() {

        this.orm = useService("orm");


        // =====================================================
        // CHART REFERENCES
        // =====================================================

        this.departmentChartRef = useRef("department_chart");
        this.zoneChartRef = useRef("zone_chart");
        this.statusChartRef = useRef("status_chart");
        this.genderChartRef = useRef("gender_chart");


        // =====================================================
        // CHART INSTANCES
        // =====================================================

        this.departmentChart = null;
        this.zoneChart = null;
        this.statusChart = null;
        this.genderChart = null;


        // =====================================================
        // STATE
        // =====================================================

        this.state = useState({

            records: [],

            posProductCount: 0,
            posConfigCount: 0,

            totalEmployees: 0,
            activeEmployees: 0,
            inactiveEmployees: 0,
            newJoiners: 0,
            exEmployees: 0,
            openPositions: 0,


            // =================================================
            // CHART DATA
            // =================================================

            departmentData: {
                labels: [],
                datasets: [],
            },

            zoneData: {
                labels: [],
                datasets: [],
            },

            statusData: {
                labels: [],
                datasets: [],
            },

            genderData: {
                labels: [],
                datasets: [],
            },

        });


        // =====================================================
        // LOAD CHART.JS
        // =====================================================

        onWillStart(async () => {

            await loadBundle("web.chartjs_lib");

        });


        // =====================================================
        // LOAD DASHBOARD
        // =====================================================

        onMounted(async () => {

            await this.loadDashboardData();

            this.renderCharts();

        });


        // =====================================================
        // CLEANUP
        // =====================================================

        onWillUnmount(() => {

            this.destroyCharts();

        });
    }


    // =========================================================
    // LOAD DASHBOARD DATA
    // =========================================================

    async loadDashboardData() {

        const data = await this.orm.call(
            "hr.employee",
            "get_dashboard_data",
            []
        );


        console.log(
            "Dashboard Data:",
            data
        );


        // =====================================================
        // KPI DATA
        // =====================================================

        this.state.totalEmployees =
            data.total_employees || 0;

        this.state.activeEmployees =
            data.active_employees || 0;

        this.state.inactiveEmployees =
            data.inactive_employees || 0;

        this.state.newJoiners =
            data.new_joiners || 0;

        this.state.exEmployees =
            data.ex_employees || 0;

        this.state.openPositions =
            data.open_positions || 0;


        // =====================================================
        // CHART DATA
        // =====================================================

        this.state.departmentData =
            data.by_department || {
                labels: [],
                datasets: [],
            };


        this.state.zoneData =
            data.by_zone || {
                labels: [],
                datasets: [],
            };


        this.state.statusData =
            data.by_status || {
                labels: [],
                datasets: [],
            };


        this.state.genderData =
            data.by_gender || {
                labels: [],
                datasets: [],
            };
    }


    // =========================================================
    // DESTROY CHARTS
    // =========================================================

    destroyCharts() {

        if (this.departmentChart) {

            this.departmentChart.destroy();

            this.departmentChart = null;
        }


        if (this.zoneChart) {

            this.zoneChart.destroy();

            this.zoneChart = null;
        }


        if (this.statusChart) {

            this.statusChart.destroy();

            this.statusChart = null;
        }


        if (this.genderChart) {

            this.genderChart.destroy();

            this.genderChart = null;
        }
    }


    // =========================================================
    // RENDER CHARTS
    // =========================================================

    renderCharts() {

        // =====================================================
        // Remove previous charts
        // =====================================================

        this.destroyCharts();


        // =====================================================
        // 1. EMPLOYEES BY DEPARTMENT
        // =====================================================

        if (this.departmentChartRef.el) {

            this.departmentChart = new window.Chart(
                this.departmentChartRef.el,
                {
                    type: "bar",

                    data: this.state.departmentData,

                    options: {

                        responsive: true,

                        maintainAspectRatio: false,


                        plugins: {

                            legend: {
                                display: false,
                            },

                        },


                        scales: {

                            y: {

                                beginAtZero: true,

                                ticks: {
                                    precision: 0,
                                },

                            },

                        },

                    },
                }
            );
        }


        // =====================================================
        // 2. EMPLOYEES BY ZONE
        // =====================================================

        if (this.zoneChartRef.el) {

            this.zoneChart = new window.Chart(
                this.zoneChartRef.el,
                {
                    type: "bar",

                    data: this.state.zoneData,

                    options: {

                        indexAxis: "y",

                        responsive: true,

                        maintainAspectRatio: false,


                        plugins: {

                            legend: {
                                display: false,
                            },

                        },


                        scales: {

                            x: {

                                beginAtZero: true,

                                ticks: {
                                    precision: 0,
                                },

                            },

                        },

                    },
                }
            );
        }


        // =====================================================
        // 3. EMPLOYEE STATUS
        // =====================================================

        if (this.statusChartRef.el) {

            this.statusChart = new window.Chart(
                this.statusChartRef.el,
                {
                    type: "doughnut",

                    data: this.state.statusData,

                    options: {

                        responsive: true,

                        maintainAspectRatio: false,


                        plugins: {

                            legend: {

                                position: "bottom",

                            },

                        },

                    },
                }
            );
        }


        // =====================================================
        // 4. EMPLOYEE GENDER RATIO
        // =====================================================

        if (this.genderChartRef.el) {

            this.genderChart = new window.Chart(
                this.genderChartRef.el,
                {
                    type: "doughnut",

                    data: this.state.genderData,

                    options: {

                        responsive: true,

                        maintainAspectRatio: false,


                        plugins: {

                            legend: {

                                position: "bottom",

                            },

                        },

                    },

                }
            );
        }

    }


    // =========================================================
    // TOTAL REVENUE
    // =========================================================

    get totalRevenue() {

        return Math.round(

            this.state.records.reduce(

                (total, record) =>

                    total +
                    (record.amount_total || 0),

                0

            )

        );
    }
}


// =============================================================
// REGISTER CLIENT ACTION
// =============================================================

registry.category("actions").add(
    "employee_dashboard.action_list_view",
    ListViewAction
);