# -*- coding: utf-8 -*-
{
    'name': 'Hotel Reservation System',
    'version': '18.0.0.0',

    'author': 'Zain Ali',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'mail', 'account', 'product', 'contacts', 'sale', 'purchase', 'za_pos_customization',
                'point_of_sale'],
    'data': [
        "data/hotel_reservation_sequence.xml",
        'security/ir.model.access.csv',
        'views/room_type_view.xml',
        'views/room_amenity_view.xml',
        'views/room_floor_view.xml',
        'views/hotel_room_view.xml',
        'views/hotel_reservation_view.xml',
        'views/menu.xml',

    ],
    # 'assets': {
    #     'point_of_sale._assets_pos': [
    #         'custom_receipts_for_pos/static/src/js/receipt_design.js',
    #         'custom_receipts_for_pos/static/src/xml/order_receipt.xml',
    #     ],
    # },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False
}
