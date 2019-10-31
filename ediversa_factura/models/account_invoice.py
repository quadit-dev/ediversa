# -*- coding: utf-8 -*-
from openerp import _, api, fields, models

class AccountTax(models.Model):
    _inherit = 'account.tax'

class AccountInvoice(models.Model):
        _name = 'account.invoice'
        _inherit = 'account.invoice'
        taxres_tipo =  fields.Many2one('account.tax',
                string = 'Impuestos totales')
