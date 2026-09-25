/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadBundle } from "@web/core/assets";

class BopChartsDashboard extends Component {
    setup() {
        this.orm = useService("orm");

        // 3 alag references create kiye
        this.chartWonLostRef = useRef("chart_won_lost");
        this.chartStageRef = useRef("chart_stage");
        this.chartTrendRef = useRef("chart_trend");

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
        });

        onMounted(() => {
            this.renderCharts();
        });
    }

    async renderCharts() {
        // Python se sara data ek saath mangwa liya
        const data = await this.orm.call(
            "crm.lead",
            "get_dashboard_data",
            []
        );

        // Chart 1: Won vs Lost (Pie)
        if (this.chartWonLostRef.el) {
            new window.Chart(this.chartWonLostRef.el, {
                type: "pie",
                data: data.won_lost,
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        // Chart 2: Leads by Stage (Bar)
        if (this.chartStageRef.el) {
            new window.Chart(this.chartStageRef.el, {
                type: "bar",
                data: data.by_stage,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        // Chart 3: Monthly Trend (Line)
        if (this.chartTrendRef.el) {
            new window.Chart(this.chartTrendRef.el, {
                type: "line",
                data: data.monthly_trend,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
    }
}

BopChartsDashboard.template = "bop_charts.Dashboard";

registry.category("actions").add(
    "bop_charts_dashboard",
    BopChartsDashboard
);

