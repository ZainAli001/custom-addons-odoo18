# -*- coding: utf-8 -*-

{
    'name': "Employee Dashboard ",
    'author': "Zain Ali Khan",
    'maintainer': "Zain Ali Khan",
    'category': 'Employee Dashboard',
    'version': '18.0.1.0.0',
    'depends': ['base', 'hr'],
    'data': [
        'views\menu.xml',
        'views\employee.xml',
    ],
    'assets': {
        # 'point_of_sale._assets_pos': [
        #
        # ],
        'web.assets_backend': [
            'employee_dashboard\static\src\components\listview.js',
            'employee_dashboard\static\src\components\listview.xml',
            'employee_dashboard\static\src\components\listview.css',
            'employee_dashboard\static\src\components\employees.js',
            'employee_dashboard\static\src\components\employees.xml',
        ],

    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,

}
