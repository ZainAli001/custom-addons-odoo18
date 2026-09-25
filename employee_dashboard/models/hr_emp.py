from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def get_dashboard_data(self):

        employees = self.search([])

        active_employees = employees.filtered(lambda e: e.active)
        inactive_employees = employees.filtered(lambda e: not e.active)

        return {
            # ==========================================
            # KPI
            # ==========================================

            "total_employees": len(employees),

            "active_employees": len(active_employees),

            "inactive_employees": len(inactive_employees),

            # ==========================================
            # Charts
            # ==========================================

            "by_department": self._get_employees_by_department(),

            "by_zone": self._get_employees_by_zone(),

            "by_status": self._get_employees_by_status(),
            "by_gender": self._get_employees_by_gender(),
        }

    # ==================================================
    # EMPLOYEES BY DEPARTMENT
    # ==================================================

    def _get_employees_by_department(self):

        groups = self.read_group(
            [],
            ["department_id"],
            ["department_id"],
        )

        labels = []
        data = []

        for group in groups:
            department = group.get("department_id")

            labels.append(
                department[1] if department else "Undefined"
            )

            data.append(
                group.get("department_id_count", 0)
            )

        return {
            "labels": labels,

            "datasets": [{
                "label": "Employees by Department",

                "data": data,

                "backgroundColor": "#17a2b8",

                "borderColor": "#117a8b",

                "borderWidth": 1,
            }],
        }

    # ==================================================
    # EMPLOYEES BY ZONE
    # ==================================================

    def _get_employees_by_zone(self):

        groups = self.read_group(
            [],
            ["zone"],
            ["zone"],
        )

        labels = []
        data = []

        for group in groups:
            zone = group.get("zone")

            labels.append(
                zone[1] if zone else "Undefined"
            )

            data.append(
                group.get("zone_count", 0)
            )

        return {
            "labels": labels,

            "datasets": [{
                "label": "Employees by Zone",

                "data": data,

                "backgroundColor": "#6f42c1",

                "borderColor": "#59359a",

                "borderWidth": 1,
            }],
        }

    # ==================================================
    # EMPLOYEE STATUS
    # ==================================================

    def _get_employees_by_status(self):

        active = self.search_count([
            ("active", "=", True)
        ])

        inactive = self.with_context(
            active_test=False
        ).search_count([
            ("active", "=", False)
        ])

        return {
            "labels": [
                "Active",
                "Inactive",
            ],

            "datasets": [{
                "label": "Employee Status",

                "data": [
                    active,
                    inactive,
                ],

                "backgroundColor": [
                    "#28a745",
                    "#dc3545",
                ],

                "borderColor": [
                    "#1e7e34",
                    "#bd2130",
                ],

                "borderWidth": 1,
            }],
        }

    # ==================================================
    # EMPLOYEE Gender
    # ==================================================

    def _get_employees_by_gender(self):
        male = self.search_count([
            ("gender", "=", 'male')
        ])
        female = self.search_count([
            ("gender", "=", 'female')
        ])
        other = self.search_count([
            ("gender", "=", 'other')
        ])

        return {
            "labels": [
                "Male",
                "Female",
                "Other",
            ],

            "datasets": [{
    "label": "Gender Ratio",

    "data": [
        male,
        female,
        other,
    ],

    "backgroundColor": [
        "#3b82f6",  # Male
        "#ec4899",  # Female
        "#8b5cf6",  # Other
    ],

    "borderColor": [
        "#2563eb",
        "#be185d",
        "#6d28d9"
    ],

    "borderWidth": 1,
}],
        }
