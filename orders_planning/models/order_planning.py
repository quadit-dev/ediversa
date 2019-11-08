# -*- coding: utf-8 -*-
# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Angel Alvarez <Developer>)
# Copyright 2019 Quadit (Lázaro Rodríguez <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import _, api, fields, models, exceptions
from datetime import datetime

class AccountInvoice(models.Model):
    _name = 'ediversa.order'
    _inherit = 'ediversa.order'

    @api.model
    def generar_orden(self, id=None):
        print "###  ------------ Crear orden de compra ---------"
        ftp_obj = self.env['ediversa.ftp']
        ftp_ids = ftp_obj.search([])
        conn = ftp_ids.test()
        change_name = ftp_ids.cambiar_nombre()

        if change_name:
            print "Cambiaron los nombres"
        else:
            print "No hay cambios realizados"

        document = ftp_ids.archivos()
        doc = open('archivos.txt', 'r')
        st = ""

        contador = 0
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y")
        for linea in doc.readlines():
            st = linea
            file = open(st, 'wb')
            conn.retrbinary('RETR %s' % st, file.write)
            file.close()
            file = open(st, 'r')
            vals = file.read()
            file.close()
            codigo = self.codigo(file,st)
            res_obj = self.env['res.partner']
            res_id = res_obj.search([('codigo_provedor','=',codigo)])
            name_order = "Order_" + date_time +"_"+ str(contador)
            ediversa_obj = self.env['ediversa.order']
            order = ediversa_obj.create({
                'subject': name_order,
                'email': res_id.email,
                'attach': vals,
                })
            attach_obj = self.env['ir.attachment']
            attach_obj.create({
                'datas': vals.encode('base64'),
                'name': linea,
                'datas_fname': 'file.txt',
                'mimetype': 'text/plain',
                'res_model': 'ediversa.order',
                'res_id': order.id,
             })
            contador = contador + 1

        conn.close()
        conn_mov = ftp_ids.mover_de_carpeta()
        print "-----------------*Termina Metodo*------------------"

    @api.multi
    def codigo(self, doc,st):
        codigo = ""
        documento = doc
        file = open(st, 'r')
        for linea in file.readlines():
            ff= linea.replace("|"," ")
            fff= ff.split(" ")[0]
            if fff == "NADMS":
                codigo = linea[6:19]
        return codigo
