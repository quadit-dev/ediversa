# -*- coding: utf-8 -*-

{
    'name': 'eDiversa Facturacion',
    'version': '9.0.1.0.0',
    'depends': [
        'mail',
        'sale',
        'purchase',
        'account'
    ],
    'author': 'Quadit, S.A. de C.V.',
    'description': 'Factura eDiversa',
    'website': 'https://www.quadit.mx',
    'data': [
        'security/factura_ediversa_security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/account_tax_view.xml',
        'wizard/factura_wizard.xml',
    ],
    'demo': [],
    'installable': True
}
