# -*- coding: utf-8 -*-
from openerp import _, api, fields, models

class account_tax(models.Model):
    _name = 'account.tax'
    _inherit = 'account.tax'
    calificador = fields.Selection([
        ('VAT', 'IVA'),
        ('IGI', 'IGIC'),
        ('EXT', 'Exento de impuesto'),
        ('ACT', 'Impuesto de alcoholes'),
        ('RE', 'Recargo de equivalencia'),
        ('ENV', 'Punto verde'),
        ('RET', 'Retenciones por servicios profesionales'),
        ('OTH', 'Otros')],
        'Calificador de tipo de impuesto',required=True, default="VAT")
