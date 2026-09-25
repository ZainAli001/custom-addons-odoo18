/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class EmployeeList extends Component {

    static template = "employee_dashboard.EmployeeList";

    setup() {

        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            employees: [],
        });

        this.loadEmployees();
    }

    async loadEmployees() {

        this.state.employees = await this.orm.searchRead(
            "hr.employee",
            [],
            [
                "name",
                "work_email",
                "department_id",
                "job_id",
            ]
        );
    }

    goDashboard() {

        this.action.doAction(
            "employee_dashboard.action_list_view"
        );

    }

}

registry.category("actions").add(
    "employee_dashboard.employee_list",
    EmployeeList
);