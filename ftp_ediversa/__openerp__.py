# -*- coding: utf-8 -*-

{
    'name': 'eDiversa FTP',
    'version': '9.0.1.0.0',
    'depends': [
        'mail',
        'sale',
        'purchase',
        'account',
        'sh_message'
    ],
    'author': 'Quadit, S.A. de C.V.',
    'description': 'eDiversa FTP',
    'website': 'https://www.quadit.mx',
    'data': [
    'security/ftp_ediversa_security.xml',
    'security/ir.model.access.csv',
    'views/ediversa_ftp.xml'
    ],
    'demo': [],
    'installable': True
}
