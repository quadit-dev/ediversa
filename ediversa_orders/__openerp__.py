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
	    'shipping_eci_corte_ingles'
    ],
    'author': 'Quadit, S.A. de C.V.',
    'description': 'eDiversa',
    'website': 'https://www.quadit.mx',
    'data': [
        'views/ediversa_sale_order.xml',
	'wizard/albaran_wizard.xml'
    ],
    'demo': [],
    'installable': True
}
