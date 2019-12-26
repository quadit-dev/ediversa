# -*- coding: utf-8 -*-

{
    'name': 'eDiversa Engine',
    'version': '9.0.1.0.0',
    'depends': [
        'mail',
        'sale',
        'purchase',
        'account',
        'tqn_partnerdiscount',
        'shipping_eci_corte_ingles',
        'delivery',
        'ftp_ediversa'
    ],
    'author': 'Quadit, S.A. de C.V.',
    'description': 'eDiversa',
    'website': 'https://www.quadit.mx',
    'data': [
        'security/orders_ediversa_security.xml',
        'security/ir.model.access.csv',
        'views/ediversa_sale_order.xml',
        'wizard/albaran_wizard.xml',
        'views/action_server_view.xml'
    ],
    'demo': [],
    'installable': True
}
