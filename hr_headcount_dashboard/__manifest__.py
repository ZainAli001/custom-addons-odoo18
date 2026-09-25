# -*- coding: utf-8 -*-
{
    'name': 'Headcount Management Dashboard',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Headcount Management dashboard with KPIs, charts and org filters',
    'description': """
Headcount Management Dashboard
===============================
Adds a Headcount Management dashboard to the HR app:

* Org master data: Region, Zone, Branch, Division, Sub-Department,
  Management Level, HR Grade.
* Extra fields on Employee: branch/zone/region/division/sub-department/
  management level/grade, employment type, employee status.
* Filterable dashboard (Region, Zone, City, Branch, Division, Department,
  Sub-Department, Designation, Management Level, HR Grade, Employment
  Type, Status, Gender, date range).
* KPI cards: Total / Active / Inactive Employees, New Joiners,
  Ex-Employees, Open Positions, Vacant Positions, On Probation.
* Charts: Headcount by Region/Zone, Headcount by Department, Employee
  Status, Gender Ratio, Full-Time vs Part-Time, Monthly Headcount Trend,
  New Joiners vs Exits, Position Status.
* Employee list with export.
    """,
    'author': 'Your Company',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['hr', 'hr_recruitment', 'hr_contract', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_management_level_data.xml',
        'views/hr_org_master_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_headcount_dashboard_views.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_headcount_dashboard/static/src/js/**/*.js',
            'hr_headcount_dashboard/static/src/xml/**/*.xml',
            'hr_headcount_dashboard/static/src/scss/**/*.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
