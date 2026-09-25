
{
    'name': 'POS Customization',
    'version': '18.0',
    'category': 'ZainAli/KOT Chit',
    'summary': 'AH KOT Chit',
    'author': 'Zain Ali',
    'depends': ['point_of_sale'],
    'data': [
        'views/res_config_view.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'za_pos_customization/static/src/xml/*.xml',
            'za_pos_customization/static/src/js/room_popup.js',
            'za_pos_customization/static/src/xml/room_popup.xml',
            'za_pos_customization/static/src/js/main.js',
            'za_pos_customization/static/src/js/pos_order.js',
            # 'za_pos_customization/static/src/js/register.js',
        ],

    },
    'installable': True,
    'application': False,
}
