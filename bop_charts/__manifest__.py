{
    'name': 'BOP Charts',
    'version': '0.1',
    'category': 'Tools',
    'depends': ['base', 'crm', 'web'],
    "data": [
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "bop_charts/static/src/js/dashboard.js",
            "bop_charts/static/src/xml/dashboard.xml",
        ],
    },

    "installable": True,
}
