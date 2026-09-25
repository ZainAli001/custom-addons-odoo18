# -*- coding: utf-8 -*-

{
    'name': "Remove Order Line In POS ",
    'summary': """
        Remove Individual Orderlines In Point Of Sale. """,
    'description': """
        Remove each lines from selected order by simply clicking X button or clear all order with a single click. 
    """,
    'author': "Cybrosys Techno Solutions",
    'website': "https://www.cybrosys.com",
    'maintainer': "Cybrosys Techno Solutions",
    'category': 'Point of Sale',
    'version': '18.0.1.0.0',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views\menu.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_delete_orderline/static/src/js/clear_button_new.js',
            # 'pos_delete_orderline/static/src/js/clear_order_line.js',
            'pos_delete_orderline/static/src/xml/clear_button.xml',
            # 'pos_delete_orderline/static/src/xml/clear_order_line.xml',
        ],
        'web.assets_backend': [
            'pos_delete_orderline\static\src\components\listview.js',
            'pos_delete_orderline\static\src\components\listview.xml',
            'pos_delete_orderline\static\src\components\listview.css'
        ],

    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,

}
