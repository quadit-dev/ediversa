# -*- coding: utf-8 -*-
# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Angel Alvarez <Developer>)
# Copyright 2019 Quadit (Lázaro Rodríguez <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import _, api, fields, models, exceptions


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
        ban = False
        # en este for se estan obteniendo todos los archivos en la carpeta Orders
        # en el servidor FTP y este manera va ejecutar el codigo de ediversa.order
        # para asi crear una orden de compra una a una
        # al final del for se moveran todos los documentos a la caperta de Records

        for linea in doc.readlines():
            print linea
            st = linea
            file = open(st, 'wb')
            conn.retrbinary('RETR %s' % st, file.write)
            file.close()
            file = open(st, 'r')
            vals = file.read()
            ediversa_obj = self.env['ediversa.order']
            order = ediversa_obj.create({
                'subject': 'Test',
                'email': 'angel.alvarez@quadit.mx',
                'attach': vals,
                })
            print order
            attach_obj = self.env['it.attachment']
            attach_obj.create({
                'datas': vals,
                'name': 'Test mimetype txt',
                'datas_fname': 'file.txt',
                'mimetype': 'text/plain',
                'res_model': 'ediversa.order',
                'res_id': order.id,
            })
            print attach_obj
