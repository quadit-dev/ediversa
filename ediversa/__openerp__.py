# -*- coding: utf-8 -*-
{
    'name': "eDiversa",

    'summary': """
        """,

    'description': """
        Módulo de integración para el servicio eDiversa.
    """,

    'author': "Quadit",
    'website': "https://www.quadit.io",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Desarrollo',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/ediversa_menu.xml',
    ]
}