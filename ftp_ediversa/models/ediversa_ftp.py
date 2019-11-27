#-*- coding: utf-8 -*-


from openerp import _, api, fields, models, exceptions
import tempfile
from ftplib import FTP
from StringIO import StringIO
import os
import datetime
import time
import shutil
import sys
import errno
import re


class sh_message_wizard(models.TransientModel):
    _name="sh.message.wizard"
    def get_default(self):
        if self.env.context.get("message",False):
            return self.env.context.get("message")
        return False


    name=fields.Text(string="Message",readonly=True,default=get_default)




class ediversaFTP(models.Model):
    _name = 'ediversa.ftp'
    _description = 'ediversa FTP'

    name_ftp = fields.Char('Nombre del FTP',required=True)
    ruta_ftp = fields.Char('Ruta del FTP',required=True)
    carpeta_orders = fields.Char('Carpeta FTP Orders', required=True)
    carpeta_invoice = fields.Char('Carpeta FTP Invoice', required=True)
    carpeta_albaran = fields.Char('Carpeta FTP Albaran', required=True)
    usuario_ftp = fields.Char('Usuario FTP', required=True)
    contrasenia_ftp = fields.Char('Contraseña FTP',required=True)


    #Devuelve una conexion de FTP con los datos ingresados por el usuario en la
    #configuracion del sistema
    @api.multi
    def test(self):
        server = self.ruta_ftp
        user = self.usuario_ftp
        passw = self.contrasenia_ftp
        try:
            conexion = FTP(server)
            conexion.login(user,passw)
            print "[+] Conexion establecida correctamente"
        except Exception as e:
            raise Warning('[-] No se pudo establecerla conexion al servidor')
            print "[-] No se pudo establecerla conexion al servidor %r" %  e
        return conexion

    #Este metodo se encarga de devolver los nombres de
    #los archivos de la carpeta donde se encuentra
    @api.multi
    def archivos(self):
        documentos = ''
        sl = '\n'
        conexion = self.test()
        conexion.cwd(self.carpeta_orders)
        if conexion:
            data=[]
            res={}
            conexion.dir(data.append)
            doc = open('archivos.txt','w+')
            for f in data:
                if f.endswith('txt'):
                    ff= f.split(" ")[-1]
                    documentos = documentos + ff + sl
                elif f.endswith('pla'):
                    ff= f.split(" ")[-1]
                    documentos = documentos + ff + sl

            doc.writelines(documentos)
            doc.close()
        conexion.close()
        return doc

    @api.multi
    def cambiar_nombre(self):
        conexion = self.test()
        conexion.cwd(self.carpeta_orders)
        doc = self.archivos()
        doc = open('archivos.txt','r')
        st =""
        ban = False
        for linea in doc.readlines():
                if linea.endswith('pla\n'):
                    sts = linea.replace('.pla\n','.txt')
                    conexion.rename(linea,sts)
                    ban = True
        return ban



    @api.multi
    def mover_de_carpeta(self):
        conexion = self.test()
        doc = self.archivos()
        st=""
        conexion.cwd(self.carpeta_orders)
        if conexion:
            doc = open('archivos.txt','r')
            for linea in doc.readlines():
                st = linea
                file = open(st, 'wb')
                conexion.retrbinary('RETR %s' % st, file.write)
                file.close()
                conexion.cwd('/')
                conexion.cwd('Records')
                file = open(st,"rb")
                conexion.storbinary("STOR "+st, file)
                conexion.retrlines("LIST")
                conexion.cwd('/')
                conexion.cwd(self.carpeta_orders)
                conexion.delete(linea)

        return conexion

    #Devuelve un mensaje si la conexion a sido exitosa
    @api.multi
    def conectar(self):
        conexion = self.test()
        if conexion:
            view = self.env.ref('ftp_ediversa.ediversa_message_wizard')
            context =dict(self._context)
            context['message'] = "[+] Conexion establecida correctamente"
        conexion.close()
        return {
            'name': 'Successfull',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id,'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    #sube una factura al servidor ftp
    @api.multi
    def subir_archivo(self,doc,name_file,namef,nom,carp):
        conexion = self.test()
        if conexion:
            if carp == "INV":
                conexion.cwd(self.carpeta_invoice)
            else:
                conexion.cwd(self.carpeta_albaran)

            documento = doc
            documento = open(name_file,"rb")
            vals= documento.read()
            fichero = open(namef,"w")
            fichero.writelines(vals)
            fichero.close()
            fichero = open(namef,"rb")
            conexion.storbinary('STOR %s' % namef, fichero)
            fichero.close()
            final = nom.replace('/','-')
            final =final+".txt"
            print namef
            print final
            conexion.retrlines("LIST")
            conexion.rename(namef,final)

            view = self.env.ref('ftp_ediversa.ediversa_message_wizard')
            context =dict(self._context)
            context['message'] = "El documento "+ str(name_file) + "esta almacenado en el servidor FTP"
        conexion.close()
        return {
            'name': 'Successfull',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id,'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    #Condicion que solo permite tener un solo registro dentro de FTP
    @api.constrains('name_ftp')
    def _check_id(self):
        print "==============>dentro del contrains"
        current_id  = self.search([('id','!=', self.id)])
        if current_id:
            raise exceptions.ValidationError("Solo puede haber un registro")





