# -*- coding: utf-8 -*-
# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Angel Alvarez <Developer>)
# Copyright 2019 Quadit (Lázaro Rodríguez <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Orders Planning ',
    'version': '9.0.1.0.0',
    'depends': [
        'mail',
        'sale',
        'purchase',
        'account',
        'sh_message',
        'ftp_ediversa',
        'ediversa_orders'
    ],
    'author': 'Quadit, S.A. de C.V.',
    'description': 'eDiversa FTP',
    'website': 'https://www.quadit.mx',
    'data': [
        'views/order_planning_view.xml'
    ],
    'demo': [],
    'installable': True
}
