#-*- coding: utf-8 -*-


from openerp import _, api, fields, models, exceptions
import tempfile
from ftplib import FTP
from StringIO import StringIO


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
    carpeta = fields.Char('Carpta FTP', required=True)
    usuario_ftp = fields.Char('Usuario FTP', required=True)
    contrasenia_ftp = fields.Char('Contraseña FTP',required=True)

    @api.multi
    def test(self):
        server = self.ruta_ftp
        user = self.usuario_ftp
        passw = self.contrasenia_ftp
        try:
            conexion = FTP(server)
            conexion.login(user,passw)
            print "[+] Conexion establecida correctamente"
        except Exception,e:
            raise Warning('[-] No se pudo establecerla conexion al servidor' + str(e))
            print "[-] No se pudo establecerla conexion al servidor" + str(e)
        return conexion

    @api.multi
    def archivos(self):
        documentos = ""
        sl = "\n"
        conexion = self.test()
        if conexion:
            #conexion.dir()
            data=[]
            res={}
            conexion.dir(data.append)
            for f in data:
                if f.endswith('txt'):
                    ff= f.split(" ")[-1]
                    documentos = documentos + ff + '\n'
            view = self.env.ref('ftp_ediversa.ediversa_message_wizard')
            context =dict(self._context)
            context['message'] = "[+] Conexion establecida correctamente" +'\n'+ documentos

        return {
            'name': 'Archivos',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id,'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }


    @api.multi
    def conectar(self):
        conexion = self.test()
        if conexion:
            view = self.env.ref('ftp_ediversa.ediversa_message_wizard')
            context =dict(self._context)
            context['message'] = "[+] Conexion establecida correctamente"

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


    @api.constrains('name_ftp')
    def _check_id(self):
        print "==============>dentro del contrains"
        current_id  = self.search([('id','!=', self.id)])
        if current_id:
            raise exceptions.ValidationError("Solo puede haber un registro")





